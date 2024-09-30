CC=gcc
CFLAGS=-I./SDL2/include
LDFLAGS=-L./src/lib -lmingw32 -lSDL2main -lSDL2

all: main

main: main.c
	$(CC) -o main main.c $(CFLAGS) $(LDFLAGS)

clean:
	rm -f main
