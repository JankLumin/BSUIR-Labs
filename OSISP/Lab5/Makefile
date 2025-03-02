CC = gcc
CFLAGS = -O2 -pthread

all: generate sort

generate: generate.c
	$(CC) $(CFLAGS) -o generate generate.c

sort: sort.c
	$(CC) $(CFLAGS) -o sort sort.c

clean:
	rm -f generate sort *.o data.txt sorted.txt sorted2.txt
