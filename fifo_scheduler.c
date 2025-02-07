/* fifo_scheduler.c */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sched.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>
#include <sys/file.h>

#define LOG_FILE "fifo_scheduler.log"
#define NUM_PROCESSES 3
#define WORK_DURATION 3  // seconds to simulate work

// Return the current time in milliseconds
long get_timestamp_ms() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (tv.tv_sec * 1000L) + (tv.tv_usec / 1000L);
}

void simulate_work() {
    sleep(WORK_DURATION);
}

void log_process_info(int process_number, pid_t pid, long start_time, long end_time) {
    FILE *fp = fopen(LOG_FILE, "a");
    if (!fp) {
        perror("fopen");
        exit(EXIT_FAILURE);
    }
    // Lock the file to prevent interleaved writes
    if (flock(fileno(fp), LOCK_EX) != 0) {
        perror("flock");
        exit(EXIT_FAILURE);
    }
    fprintf(fp, "Process %d (PID=%d), start=%ld ms, end=%ld ms\n", process_number, pid, start_time, end_time);
    fflush(fp);
    flock(fileno(fp), LOCK_UN);
    fclose(fp);
}

int main(int argc, char *argv[]) {
    int i;

    // Clear (or create) the log file at startup
    FILE *fp = fopen(LOG_FILE, "w");
    if (fp) {
        fclose(fp);
    } else {
        perror("fopen");
    }

    for (i = 0; i < NUM_PROCESSES; i++) {
        pid_t pid = fork();
        if (pid < 0) {
            perror("fork");
            exit(EXIT_FAILURE);
        }
        if (pid == 0) {
            // In the child process
            struct sched_param param;
            param.sched_priority = 50;  // Fixed priority for FIFO scheduler
            if (sched_setscheduler(0, SCHED_FIFO, &param) == -1) {
                fprintf(stderr, "Child PID %d: sched_setscheduler failed: %s\n", getpid(), strerror(errno));
                exit(EXIT_FAILURE);
            }
            long start_time = get_timestamp_ms();
            printf("Process %d (PID=%d) starting work at %ld ms\n", i + 1, getpid(), start_time);
            simulate_work();
            long end_time = get_timestamp_ms();
            printf("Process %d (PID=%d) finished work at %ld ms\n", i + 1, getpid(), end_time);
            log_process_info(i + 1, getpid(), start_time, end_time);
            exit(EXIT_SUCCESS);
        }
        usleep(100000); // 100 ms delay for clarity
    }

    // Wait for all children to finish
    for (i = 0; i < NUM_PROCESSES; i++) {
        wait(NULL);
    }
    printf("All child processes have completed.\n");
    return 0;
}
