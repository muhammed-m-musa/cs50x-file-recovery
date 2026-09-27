# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -std=c11

# The final executable name
TARGET = project

# Source files and object files
SRCS = main.c organizer.c recover.c
OBJS = $(SRCS:.c=.o)

# Default rule
all: $(TARGET)

# Explicit target so 'make project' works directly
project: $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

# Compile source files into object files with header dependencies
%.o: %.c recover.h organizer.h
	$(CC) $(CFLAGS) -c $< -o $@

# Clean up build files
clean:
	rm -f $(TARGET) *.o organizer_report.csv
