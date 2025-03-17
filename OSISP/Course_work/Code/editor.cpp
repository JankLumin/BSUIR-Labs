#include "editor.h"
#include <ctype.h>
#include <fcntl.h>
#include <linux/fs.h>
#include <ncurses.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <vector>

// Количество байт в строке
#define BYTES_PER_ROW 16

// Структура для undo/redo
struct Change {
  char op; // 'E' - edit byte, 'P' - paste
  int sector; // какому сектору принадлежит изменение
  int offset; // для 'E': смещение байта
  unsigned char oldValue;
  unsigned char newValue;
  std::vector<unsigned char> oldSector; // для 'P'
  std::vector<unsigned char> newSector; // для 'P'
};

// Глобальные переменные
static int fd = -1;
static unsigned long long deviceSize;
static int sectorSizeGlobal = 512;
static int numSectors = 0;
static bool autosave = false;

// Текущее состояние
static int currentSector = 0;
static int cursorX = 0, cursorY = 0;

// Undo/Redo стеки
static std::vector<Change> undoStack;
static std::vector<Change> redoStack;

// Буфер для текущего сектора
static std::vector<unsigned char> sectorBuffer;
static bool sectorBufferLoaded = false;

// Буфер для копирования сектора
static std::vector<unsigned char> copyBuffer;
static bool hasCopy = false;

// Вспомогательные функции

static inline int getIndexInBuffer(int row, int col) {
  return row * BYTES_PER_ROW + col;
}

// Загрузить текущий сектор (currentSector) в sectorBuffer
static bool loadCurrentSector() {
  if (currentSector < 0 || currentSector >= numSectors)
    return false;
  sectorBufferLoaded = false;
  sectorBuffer.resize(sectorSizeGlobal, 0);

  off_t offset = (off_t)currentSector * sectorSizeGlobal;
  ssize_t r = pread(fd, sectorBuffer.data(), sectorSizeGlobal, offset);
  if (r != (ssize_t)sectorSizeGlobal) {
    return false;
  }
  sectorBufferLoaded = true;
  return true;
}

// Сохранить sectorBuffer в текущий сектор
static bool saveCurrentSector() {
  if (!sectorBufferLoaded)
    return false;
  off_t offset = (off_t)currentSector * sectorSizeGlobal;
  ssize_t w = pwrite(fd, sectorBuffer.data(), sectorSizeGlobal, offset);
  return (w == (ssize_t)sectorSizeGlobal);
}

// Отрисовка UI
static void drawUI(const char *filename) {
  clear();
  mvprintw(0, 0, "File: %s | Sector: %d/%d | Sector size: %d bytes", filename,
           currentSector, numSectors - 1, sectorSizeGlobal);

  if (!sectorBufferLoaded) {
    mvprintw(2, 0, "Error: sector not loaded!");
    refresh();
    return;
  }

  int rows = sectorSizeGlobal / BYTES_PER_ROW;
  for (int row = 0; row < rows; row++) {
    int offset = row * BYTES_PER_ROW;
    mvprintw(row + 1, 0, "%04X: ", offset);
    for (int col = 0; col < BYTES_PER_ROW; col++) {
      int index = offset + col;
      unsigned char byteVal = sectorBuffer[index];
      if (row == cursorY && col == cursorX) {
        attron(A_REVERSE);
        printw("%02X ", byteVal);
        attroff(A_REVERSE);
      } else {
        printw("%02X ", byteVal);
      }
    }
    printw("  ");
    for (int col = 0; col < BYTES_PER_ROW; col++) {
      int index = offset + col;
      unsigned char byteVal = sectorBuffer[index];
      if (isprint(byteVal)) {
        printw("%c", byteVal);
      } else {
        printw(".");
      }
    }
  }
  int bottom = (sectorSizeGlobal / BYTES_PER_ROW) + 2;
  // Краткая справка внизу
  mvprintw(bottom, 0,
           "Arrows: move cursor | n/p: next/prev sector | j: jump sector");
  mvprintw(bottom + 1, 0,
           "e/Enter: edit byte | s: save | c: copy | v: paste | u:undo | "
           "r:redo | h:help | q:quit");
  refresh();
}

// Переместить курсор
static void moveCursor(int dy, int dx) {
  int rows = sectorSizeGlobal / BYTES_PER_ROW;
  cursorY += dy;
  cursorX += dx;
  if (cursorY < 0)
    cursorY = 0;
  if (cursorY >= rows)
    cursorY = rows - 1;
  if (cursorX < 0)
    cursorX = 0;
  if (cursorX >= BYTES_PER_ROW)
    cursorX = BYTES_PER_ROW - 1;
}

// Подробная помощь (при нажатии h)
static void showDetailedHelp() {
  clear();
  int row = 0;
  attron(A_BOLD);
  mvprintw(row++, 0, "Low-Level Sector Editor - Detailed Help");
  attroff(A_BOLD);
  row++;
  mvprintw(row++, 0,
           "This editor allows viewing and editing of raw sectors from a file "
           "or block device.");
  mvprintw(row++, 0,
           "You can navigate inside each sector using the arrow keys. Each "
           "sector is displayed");
  mvprintw(row++, 0, "in both hexadecimal and ASCII format, 16 bytes per row.");
  row++;
  mvprintw(row++, 0, "Controls:");
  mvprintw(row++, 0,
           "  Arrow keys  : Move the cursor within the current sector "
           "(up/down/left/right)");
  mvprintw(row++, 0, "  n/p         : Go to the next/previous sector");
  mvprintw(row++, 0,
           "  j           : Jump to a specific sector by entering its number");
  mvprintw(row++, 0,
           "  e or Enter  : Edit the byte under the cursor (enter a 2-digit "
           "HEX value)");
  mvprintw(row++, 0,
           "  s           : Save the current sector to the file/device");
  mvprintw(row++, 0, "  c           : Copy the entire sector into a buffer");
  mvprintw(row++, 0,
           "  v           : Paste the copied sector into the current sector "
           "(overwrites data)");
  mvprintw(row++, 0,
           "  u/r         : Undo/redo changes (including single-byte edits or "
           "entire paste operations)");
  mvprintw(row++, 0, "  h           : Show this detailed help screen");
  mvprintw(row++, 0, "  q           : Quit the editor");
  row++;
  mvprintw(row++, 0, "Press any key to return...");
  refresh();
  getch();
}

// Редактирование байта под курсором
static void editByte() {
  if (!sectorBufferLoaded)
    return;
  int offset = cursorY * BYTES_PER_ROW + cursorX;
  echo();
  curs_set(1);

  mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 4, 0,
           "Enter new HEX (2 digits) for offset %04X: ", offset);
  clrtoeol();
  char input[3] = {0};
  getnstr(input, 2);

  int newVal;
  if (sscanf(input, "%x", &newVal) == 1 && newVal >= 0 && newVal <= 255) {
    unsigned char oldVal = sectorBuffer[offset];
    if (oldVal != (unsigned char)newVal) {
      // Undo entry
      Change ch;
      ch.op = 'E';
      ch.sector = currentSector;
      ch.offset = offset;
      ch.oldValue = oldVal;
      ch.newValue = (unsigned char)newVal;
      undoStack.push_back(ch);
      redoStack.clear();
    }
    sectorBuffer[offset] = (unsigned char)newVal;

    if (autosave) {
      if (!saveCurrentSector()) {
        mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 5, 0,
                 "Error writing sector!");
        getch();
      }
    }
  } else {
    mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 5, 0,
             "Invalid input! Press any key...");
    getch();
  }
  noecho();
  curs_set(0);
}

// Сохранение сектора
static void saveSector(bool showMessage) {
  if (!sectorBufferLoaded)
    return;
  if (!saveCurrentSector()) {
    mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 6, 0,
             "Error writing sector!");
    getch();
  } else {
    if (showMessage) {
      mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 6, 0,
               "Sector saved. Press any key...");
      getch();
    }
  }
}

// Undo
static void undoChange() {
  if (undoStack.empty())
    return;
  Change ch = undoStack.back();
  undoStack.pop_back();

  // Возможно, надо перейти в другой сектор
  if (ch.sector != currentSector) {
    if (autosave)
      saveCurrentSector();
    currentSector = ch.sector;
    loadCurrentSector();
    cursorX = 0;
    cursorY = 0;
  }

  if (ch.op == 'E') {
    // один байт
    sectorBuffer[ch.offset] = ch.oldValue;
  } else if (ch.op == 'P') {
    // вернуть старый сектор
    memcpy(sectorBuffer.data(), ch.oldSector.data(), sectorSizeGlobal);
  }

  redoStack.push_back(ch);
  if (autosave)
    saveCurrentSector();
  mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 6, 0,
           "Undo done. Press any key...");
  getch();
}

// Redo
static void redoChange() {
  if (redoStack.empty())
    return;
  Change ch = redoStack.back();
  redoStack.pop_back();

  if (ch.sector != currentSector) {
    if (autosave)
      saveCurrentSector();
    currentSector = ch.sector;
    loadCurrentSector();
    cursorX = 0;
    cursorY = 0;
  }

  if (ch.op == 'E') {
    sectorBuffer[ch.offset] = ch.newValue;
  } else if (ch.op == 'P') {
    memcpy(sectorBuffer.data(), ch.newSector.data(), sectorSizeGlobal);
  }
  undoStack.push_back(ch);
  if (autosave)
    saveCurrentSector();
  mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 6, 0,
           "Redo done. Press any key...");
  getch();
}

// Копирование сектора
static void copySector() {
  if (!sectorBufferLoaded)
    return;
  copyBuffer.resize(sectorSizeGlobal);
  memcpy(copyBuffer.data(), sectorBuffer.data(), sectorSizeGlobal);
  hasCopy = true;
  mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 5, 0,
           "Sector copied. Press any key...");
  getch();
}

// Вставка сектора
static void pasteSector() {
  if (!sectorBufferLoaded)
    return;
  if (!hasCopy) {
    mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 5, 0,
             "No sector copied. Press any key...");
    getch();
    return;
  }
  mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 5, 0, "Confirm paste? (y/n): ");
  int c = getch();
  if (c != 'y' && c != 'Y') {
    mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 6, 0,
             "Paste cancelled. Press any key...");
    getch();
    return;
  }
  Change ch;
  ch.op = 'P';
  ch.sector = currentSector;
  ch.oldSector.resize(sectorSizeGlobal);
  ch.newSector.resize(sectorSizeGlobal);

  memcpy(ch.oldSector.data(), sectorBuffer.data(), sectorSizeGlobal);
  memcpy(sectorBuffer.data(), copyBuffer.data(), sectorSizeGlobal);
  memcpy(ch.newSector.data(), sectorBuffer.data(), sectorSizeGlobal);

  undoStack.push_back(ch);
  redoStack.clear();

  if (autosave)
    saveCurrentSector();
  mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 6, 0,
           "Sector pasted. Press any key...");
  getch();
}

// Переход к следующему сектору
static void nextSector() {
  if (currentSector < numSectors - 1) {
    if (autosave)
      saveCurrentSector();
    currentSector++;
    loadCurrentSector();
    cursorX = 0;
    cursorY = 0;
  }
}

// Переход к предыдущему сектору
static void prevSector() {
  if (currentSector > 0) {
    if (autosave)
      saveCurrentSector();
    currentSector--;
    loadCurrentSector();
    cursorX = 0;
    cursorY = 0;
  }
}

// Переход к указанному сектору
static void jumpSector() {
  echo();
  curs_set(1);
  mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 5, 0,
           "Enter sector number (0..%d): ", numSectors - 1);
  char buf[32];
  getnstr(buf, 31);
  noecho();
  curs_set(0);

  int s = atoi(buf);
  if (s >= 0 && s < numSectors) {
    if (autosave)
      saveCurrentSector();
    currentSector = s;
    if (!loadCurrentSector()) {
      mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 6, 0,
               "Error reading sector! Press any key...");
      getch();
    }
    cursorX = 0;
    cursorY = 0;
  } else {
    mvprintw((sectorSizeGlobal / BYTES_PER_ROW) + 6, 0,
             "Invalid sector! Press any key...");
    getch();
  }
}

// Основная функция
void runEditor(const char *filename, int secSize, bool autosaveFlag) {
  sectorSizeGlobal = secSize;
  autosave = autosaveFlag;

  fd = open(filename, O_RDWR);
  if (fd < 0) {
    perror("Error opening file/device");
    exit(EXIT_FAILURE);
  }

  // Определяем размер
  unsigned long long size64 = 0;
  if (ioctl(fd, BLKGETSIZE64, &size64) == 0 && size64 > 0) {
    deviceSize = size64;
  } else {
    off_t sz = lseek(fd, 0, SEEK_END);
    if (sz < 0) {
      perror("lseek");
      close(fd);
      exit(EXIT_FAILURE);
    }
    deviceSize = (unsigned long long)sz;
  }

  // Число секторов
  numSectors = deviceSize / sectorSizeGlobal;
  if (deviceSize % sectorSizeGlobal != 0) {
    numSectors++;
  }

  // Готовим буфер для одного сектора
  sectorBuffer.resize(sectorSizeGlobal, 0);
  sectorBufferLoaded = false;

  copyBuffer.resize(sectorSizeGlobal, 0);
  hasCopy = false;

  currentSector = 0;
  if (!loadCurrentSector()) {
    printf("Error reading first sector.\n");
    close(fd);
    return;
  }

  // Инициализация ncurses
  initscr();
  if (has_colors()) {
    start_color();
    init_pair(1, COLOR_WHITE, COLOR_BLACK);
    init_pair(2, COLOR_RED, COLOR_BLACK);
  }
  noecho();
  cbreak();
  keypad(stdscr, TRUE);
  curs_set(0);

  int ch;
  while (true) {
    drawUI(filename);
    ch = getch();
    if (ch == 'q') {
      break;
    } else if (ch == KEY_UP) {
      moveCursor(-1, 0);
    } else if (ch == KEY_DOWN) {
      moveCursor(1, 0);
    } else if (ch == KEY_LEFT) {
      moveCursor(0, -1);
    } else if (ch == KEY_RIGHT) {
      moveCursor(0, 1);
    } else if (ch == 'n') {
      nextSector();
    } else if (ch == 'p') {
      prevSector();
    } else if (ch == 'j') {
      jumpSector();
    } else if (ch == 'e' || ch == '\n') {
      editByte();
    } else if (ch == 's') {
      saveSector(true);
    } else if (ch == 'c' || ch == 'C') {
      copySector();
    } else if (ch == 'v' || ch == 'V') {
      pasteSector();
    } else if (ch == 'u' || ch == 'U') {
      undoChange();
    } else if (ch == 'r' || ch == 'R') {
      redoChange();
    } else if (ch == 'h') {
      showDetailedHelp();
    }
  }

  endwin();
  close(fd);
}
