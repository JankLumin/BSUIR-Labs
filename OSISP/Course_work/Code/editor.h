#ifndef EDITOR_H
#define EDITOR_H

// Запуск редактора с поддержкой undo/redo, без загрузки всего устройства в
// память. filename: имя файла или блочного устройства, sectorSize: размер
// сектора (по умолчанию 512), autosave: флаг автосохранения (true/false).
void runEditor(const char *filename, int sectorSize, bool autosave);

#endif // EDITOR_H
