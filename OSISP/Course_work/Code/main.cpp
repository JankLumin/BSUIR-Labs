#include "editor.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>

static void printUsage(const char *progName) {
  printf("Usage: %s [--help] [--autosave] <image file> [sector size]\n",
         progName);
}

int main(int argc, char *argv[]) {
  bool autosave = false;
  const char *filename = NULL;
  int sectorSize = 512;

  if (argc < 2) {
    printUsage(argv[0]);
    return EXIT_FAILURE;
  }

  int argIndex = 1;
  while (argIndex < argc && strncmp(argv[argIndex], "--", 2) == 0) {
    if (strcmp(argv[argIndex], "--help") == 0) {
      printUsage(argv[0]);
      printf("\nLow-Level Sector Editor\n");
      printf("Options:\n  --autosave   Automatically save after editing\n");
      return EXIT_SUCCESS;
    } else if (strcmp(argv[argIndex], "--autosave") == 0) {
      autosave = true;
    } else {
      printUsage(argv[0]);
      return EXIT_FAILURE;
    }
    argIndex++;
  }

  if (argIndex < argc) {
    filename = argv[argIndex++];
  } else {
    printUsage(argv[0]);
    return EXIT_FAILURE;
  }

  if (argIndex < argc) {
    sectorSize = atoi(argv[argIndex]);
    if (sectorSize <= 0)
      sectorSize = 512;
  }

  runEditor(filename, sectorSize, autosave);
  return EXIT_SUCCESS;
}
