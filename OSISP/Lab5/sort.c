#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

#define NUM_THREADS 20

int cmpfunc(const void *a, const void *b) {
  int int_a = *(int *)a;
  int int_b = *(int *)b;
  return int_a - int_b;
}

int *read_data(const char *filename, int *n_out) {
  FILE *fp = fopen(filename, "r");
  if (!fp) {
    perror("Ошибка открытия входного файла");
    exit(EXIT_FAILURE);
  }
  int n;
  if (fscanf(fp, "%d", &n) != 1) {
    fprintf(stderr, "Ошибка чтения количества элементов\n");
    exit(EXIT_FAILURE);
  }
  int *arr = malloc(n * sizeof(int));
  if (!arr) {
    perror("Ошибка выделения памяти");
    exit(EXIT_FAILURE);
  }
  for (int i = 0; i < n; i++) {
    if (fscanf(fp, "%d", &arr[i]) != 1) {
      fprintf(stderr, "Ошибка чтения элемента %d\n", i);
      exit(EXIT_FAILURE);
    }
  }
  fclose(fp);
  *n_out = n;
  return arr;
}

void write_array_to_file(const char *filename, int *arr, int n) {
  FILE *fp = fopen(filename, "w");
  if (!fp) {
    perror("Ошибка открытия выходного файла");
    exit(EXIT_FAILURE);
  }
  fprintf(fp, "%d\n", n);
  for (int i = 0; i < n; i++) {
    fprintf(fp, "%d ", arr[i]);
  }
  fclose(fp);
}

typedef struct {
  int *array;
  int left;
  int right;
} ThreadData;

void *thread_sort(void *arg) {
  ThreadData *data = (ThreadData *)arg;
  qsort(data->array + data->left, data->right - data->left, sizeof(int),
        cmpfunc);
  pthread_exit(NULL);
}

void merge(int *arr, int left, int mid, int right, int *aux) {
  int i = left, j = mid, k = left;
  while (i < mid && j < right) {
    if (arr[i] <= arr[j])
      aux[k++] = arr[i++];
    else
      aux[k++] = arr[j++];
  }
  while (i < mid)
    aux[k++] = arr[i++];
  while (j < right)
    aux[k++] = arr[j++];
  for (i = left; i < right; i++)
    arr[i] = aux[i];
}

typedef struct {
  int left;
  int right;
} Segment;

int main() {
  const char *input_file = "data.txt";
  int n;
  int *orig_array = read_data(input_file, &n);
  printf("Прочитано %d элементов из файла %s\n", n, input_file);

  int *array_multithread = malloc(n * sizeof(int));
  int *array_singlethread = malloc(n * sizeof(int));
  if (!array_multithread || !array_singlethread) {
    perror("Ошибка выделения памяти");
    exit(EXIT_FAILURE);
  }
  memcpy(array_multithread, orig_array, n * sizeof(int));
  memcpy(array_singlethread, orig_array, n * sizeof(int));
  free(orig_array);

  struct timeval start, end;
  double elapsed_multithread, elapsed_singlethread;

  pthread_t threads[NUM_THREADS];
  ThreadData threadData[NUM_THREADS];
  int seg_size = n / NUM_THREADS;
  for (int i = 0; i < NUM_THREADS; i++) {
    threadData[i].array = array_multithread;
    threadData[i].left = i * seg_size;
    threadData[i].right = (i == NUM_THREADS - 1) ? n : (i + 1) * seg_size;
  }
  gettimeofday(&start, NULL);
  for (int i = 0; i < NUM_THREADS; i++) {
    if (pthread_create(&threads[i], NULL, thread_sort, &threadData[i]) != 0) {
      perror("Ошибка создания потока");
      exit(EXIT_FAILURE);
    }
  }
  for (int i = 0; i < NUM_THREADS; i++) {
    pthread_join(threads[i], NULL);
  }
  int *aux = malloc(n * sizeof(int));
  if (!aux) {
    perror("Ошибка выделения памяти для вспомогательного массива");
    exit(EXIT_FAILURE);
  }
  Segment segments[NUM_THREADS];
  for (int i = 0; i < NUM_THREADS; i++) {
    segments[i].left = threadData[i].left;
    segments[i].right = threadData[i].right;
  }
  int numSegments = NUM_THREADS;
  while (numSegments > 1) {
    int newCount = (numSegments + 1) / 2;
    for (int i = 0; i < numSegments / 2; i++) {
      int left = segments[2 * i].left;
      int mid = segments[2 * i].right;
      int right = segments[2 * i + 1].right;
      merge(array_multithread, left, mid, right, aux);
      segments[i].left = left;
      segments[i].right = right;
    }
    if (numSegments % 2 == 1) {
      segments[newCount - 1] = segments[numSegments - 1];
    }
    numSegments = newCount;
  }
  gettimeofday(&end, NULL);
  elapsed_multithread = (end.tv_sec - start.tv_sec) * 1000.0 +
                        (end.tv_usec - start.tv_usec) / 1000.0;
  printf("Время многопоточной сортировки: %.3f мс\n", elapsed_multithread);

  gettimeofday(&start, NULL);
  qsort(array_singlethread, n, sizeof(int), cmpfunc);
  gettimeofday(&end, NULL);
  elapsed_singlethread = (end.tv_sec - start.tv_sec) * 1000.0 +
                         (end.tv_usec - start.tv_usec) / 1000.0;
  printf("Время однопоточной сортировки: %.3f мс\n", elapsed_singlethread);

  write_array_to_file("sorted2.txt", array_multithread, n);
  write_array_to_file("sorted.txt", array_singlethread, n);
  printf("Отсортированные массивы записаны в файлы 'sorted2.txt' "
         "(многопоточная) и 'sorted.txt' (однопоточная).\n");

  free(array_multithread);
  free(array_singlethread);
  free(aux);
  return 0;
}
