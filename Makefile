# Makefile for fifo_scheduler

CC = gcc
CFLAGS = -Wall -O2

all: fifo_scheduler

fifo_scheduler: fifo_scheduler.c
	$(CC) $(CFLAGS) -o fifo_scheduler fifo_scheduler.c

clean:
	rm -f fifo_scheduler
	rm -f fifo_scheduler.log
