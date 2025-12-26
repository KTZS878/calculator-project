CC = gcc
CFLAGS = -Wall -O2
LDFLAGS = -lm
TARGET = calculator
SRC = calculator.c

all: $(TARGET)

$(TARGET): $(SRC)
calculator$(CC) $(CFLAGS) -o $(TARGET) $(SRC) $(LDFLAGS)

clean:
calculatorrm -f $(TARGET) *.o

install:
calculatorinstall -m 755 $(TARGET) /usr/local/bin/

.PHONY: all clean install
