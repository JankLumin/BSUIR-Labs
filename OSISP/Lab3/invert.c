#include "invert.h"
#include <string.h>

static void reverse_substring(char *line, int start, int end) {
  while (start < end) {
    char temp = line[start];
    line[start] = line[end];
    line[end] = temp;
    start++;
    end--;
  }
}

void reverse_words_in_line(char *line) {
  int length = (int)strlen(line);
  int i = 0;

  while (i < length) {
    while (i < length && (line[i] == ' ' || line[i] == '\t')) {
      i++;
    }

    if (i < length && line[i] == '\n') {
      break;
    }

    int start = i;

    while (i < length && line[i] != ' ' && line[i] != '\t' && line[i] != '\n') {
      i++;
    }

    int end = i - 1;

    if (start < end) {
      reverse_substring(line, start, end);
    }
  }
}
