#include <csignal>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <unistd.h>

volatile sig_atomic_t counter = 0;

void handle_signal(int sig) {
  std::cout << "\nПолучен сигнал " << sig << ". Запуск нового процесса..."
            << std::endl;

  pid_t pid = fork();
  if (pid < 0) {
    perror("Ошибка fork");
    exit(EXIT_FAILURE);
  } else if (pid > 0) {
    std::cout << "Родительский процесс завершает работу." << std::endl;
    exit(EXIT_SUCCESS);
  } else {
    std::cout << "Новый процесс продолжает выполнение. Счётчик = " << counter
              << std::endl;
  }
}

int main() {
  struct sigaction sa;
  sa.sa_handler = handle_signal;
  sa.sa_flags = SA_RESTART;
  sigemptyset(&sa.sa_mask);

  if (sigaction(SIGTERM, &sa, nullptr) == -1) {
    perror("Ошибка установки обработчика SIGTERM");
    exit(EXIT_FAILURE);
  }
  if (sigaction(SIGINT, &sa, nullptr) == -1) {
    perror("Ошибка установки обработчика SIGINT");
    exit(EXIT_FAILURE);
  }

  while (true) {
    counter++;
    std::cout << "Счётчик: " << counter << std::endl;

    std::ofstream out("counter.txt", std::ios::app);
    if (out) {
      out << "Счётчик: " << counter << std::endl;
    } else {
      perror("Не удалось открыть counter.txt");
    }

    sleep(1);
  }

  return 0;
}

// pgrep -f self_recovering_process
// kill -TERM <PID>
// pkill -9 -f self_recovering_process
