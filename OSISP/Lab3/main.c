#define _XOPEN_SOURCE 700
#include "invert.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define MAX_LINE_LENGTH 1024

void print_usage(const char *progname) {
  fprintf(stderr, "Usage: %s [-i input_file] [-o output_file]\n", progname);
  fprintf(stderr,
          "  -i input_file   Указать входной файл (по умолчанию: stdin)\n");
  fprintf(stderr,
          "  -o output_file  Указать выходной файл (по умолчанию: stdout)\n");
  fprintf(stderr, "  -h              Показать справку\n");
}

int main(int argc, char *argv[]) {
  int opt;
  const char *input_filename = NULL;
  const char *output_filename = NULL;
  FILE *fin = stdin;
  FILE *fout = stdout;
  char buffer[MAX_LINE_LENGTH];

  while ((opt = getopt(argc, argv, "i:o:h")) != -1) {
    switch (opt) {
    case 'i':
      input_filename = optarg;
      break;
    case 'o':
      output_filename = optarg;
      break;
    case 'h':
      print_usage(argv[0]);
      return 0;
    default:
      print_usage(argv[0]);
      return 1;
    }
  }

  if (input_filename) {
    fin = fopen(input_filename, "r");
    if (!fin) {
      perror("Ошибка открытия входного файла");
      return 1;
    }
  }

  if (output_filename) {
    fout = fopen(output_filename, "w");
    if (!fout) {
      perror("Ошибка открытия выходного файла");
      if (fin != stdin) {
        fclose(fin);
      }
      return 1;
    }
  }

  while (fgets(buffer, MAX_LINE_LENGTH, fin) != NULL) {
    reverse_words_in_line(buffer);
    fputs(buffer, fout);
  }

  if (fin != stdin) {
    fclose(fin);
  }
  if (fout != stdout) {
    fclose(fout);
  }

  return 0;
}
