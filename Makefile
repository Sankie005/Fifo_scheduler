# Makefile for FIFO, LIFO, and FIFO Round-Robin schedulers

CC = gcc
CFLAGS = -Wall -O2

all: fifo_scheduler lifo_scheduler fifo_rr_scheduler

fifo_scheduler: fifo_scheduler.c
	$(CC) $(CFLAGS) -o fifo_scheduler fifo_scheduler.c

lifo_scheduler: lifo_scheduler.c
	$(CC) $(CFLAGS) -o lifo_scheduler lifo_scheduler.c

fifo_rr_scheduler: fifo_rr_scheduler.c
	$(CC) $(CFLAGS) -o fifo_rr_scheduler fifo_rr_scheduler.c

clean:
	rm -f fifo_scheduler lifo_scheduler fifo_rr_scheduler
	rm -f fifo_scheduler.log lifo_scheduler.log fifo_rr_scheduler.log
