/* lifo_scheduler.c */
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

#define LOG_FILE "lifo_scheduler.log"
#define NUM_PROCESSES 3
#define WORK_DURATION 3  // seconds to simulate work

// Return the current time in milliseconds
long get_timestamp_ms() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (tv.tv_sec * 1000L) + (tv.tv_usec / 1000L);
}

void simulate_work(int process_id) {
    printf("Process %d is working...\n", process_id);
    sleep(WORK_DURATION);
}

void log_process_info(int process_id, pid_t pid, long start_time, long end_time) {
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
    fprintf(fp, "Process %d (PID=%d), start=%ld ms, end=%ld ms\n", process_id, pid, start_time, end_time);
    fflush(fp);
    flock(fileno(fp), LOCK_UN);
    fclose(fp);
}

int main(int argc, char *argv[]) {
    int i;
    struct sched_param param;

    // Clear (or create) the log file at startup
    FILE *fp = fopen(LOG_FILE, "w");
    if (fp) {
        fclose(fp);
    } else {
        perror("fopen");
    }

    // Fork processes in reverse order to enforce LIFO execution
    for (i = NUM_PROCESSES - 1; i >= 0; i--) {
        pid_t pid = fork();
        if (pid < 0) {
            perror("fork");
            exit(EXIT_FAILURE);
        }
        if (pid == 0) {
            // Child process
            int process_id = NUM_PROCESSES - i;  // Process names: 1, 2, 3
            param.sched_priority = 50 + (NUM_PROCESSES - i);

            if (sched_setscheduler(0, SCHED_FIFO, &param) == -1) {
                fprintf(stderr, "Child PID %d: sched_setscheduler failed: %s\n", getpid(), strerror(errno));
                exit(EXIT_FAILURE);
            }

            // Wait for a slight delay to enforce LIFO behavior
            sleep(NUM_PROCESSES - process_id);

            long start_time = get_timestamp_ms();
            printf("Process %d (PID %d) starting work with priority %d at %ld ms\n",
                   process_id, getpid(), param.sched_priority, start_time);
            simulate_work(process_id);
            long end_time = get_timestamp_ms();
            printf("Process %d (PID %d) finished work at %ld ms\n", process_id, getpid(), end_time);
            log_process_info(process_id, getpid(), start_time, end_time);
            exit(EXIT_SUCCESS);
        }
        usleep(100000); // slight delay between forks
    }

    // Parent process waits for all child processes
    for (i = 0; i < NUM_PROCESSES; i++) {
        wait(NULL);
    }

    printf("All child processes have completed.\n");
    return 0;
}
