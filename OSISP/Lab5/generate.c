#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void generate_test_file(const char *filename, int n) {
  FILE *f = fopen(filename, "w");
  if (!f) {
    perror("Ошибка открытия файла для записи");
    exit(EXIT_FAILURE);
  }
  fprintf(f, "%d\n", n);
  for (int i = 0; i < n; i++) {
    int num = rand() % 1000000;
    fprintf(f, "%d ", num);
  }
  fclose(f);
  printf("Файл '%s' с %d элементами успешно создан.\n", filename, n);
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    fprintf(stderr, "Использование: %s <количество элементов>\n", argv[0]);
    return 1;
  }
  const char *filename = "data.txt";
  int n = atoi(argv[1]);
  srand(time(NULL));
  generate_test_file(filename, n);
  return 0;
}
