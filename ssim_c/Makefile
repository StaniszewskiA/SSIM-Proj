CC = gcc
CFLAGS = -I./src/include
LDFLAGS = -L./src/lib -lmingw32 -lSDL2main -lSDL2
TARGET = main
SRC = main.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) -o $@ $< $(CFLAGS) $(LDFLAGS)

clean:
	rm -f $(TARGET)
