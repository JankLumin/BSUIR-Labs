CC = gcc
CFLAGS = -Wall -Wextra -std=c11
TARGET = invert_chars
OBJS = main.o invert.o

.PHONY: all clean test

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

main.o: main.c invert.h
	$(CC) $(CFLAGS) -c main.c

invert.o: invert.c invert.h
	$(CC) $(CFLAGS) -c invert.c

clean:
	rm -f $(OBJS)

test: all
	@echo "==== Запуск теста ===="
	./$(TARGET) -i input.txt -o output.txt
	@echo "Результат записан в output.txt"
	@echo "==== Тест завершён ===="
