#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/time.h>

#define TIME_QUANTUM 500  // Time quantum in milliseconds
#define MAX_PROCESSES 10

typedef struct {
    pid_t pid;
    int remaining_time;
} Process;

Process process_queue[MAX_PROCESSES];
int process_count = 0;
int current_process = 0;
struct itimerval timer;

// Signal handler for the timer
void timer_handler(int signum) {
    if (process_count == 0) return;

    // Reduce remaining time of the current process
    process_queue[current_process].remaining_time -= TIME_QUANTUM;

    if (process_queue[current_process].remaining_time > 0) {
        // Pause the current process
        if (kill(process_queue[current_process].pid, SIGSTOP) == 0) {
            printf("Process %d (PID=%d) paused, remaining time: %d ms\n", 
                current_process + 1, process_queue[current_process].pid, 
                process_queue[current_process].remaining_time);
        }
    } else {
        // Process completed
        printf("Process %d (PID=%d) finished execution.\n", 
            current_process + 1, process_queue[current_process].pid);
        kill(process_queue[current_process].pid, SIGKILL);
        waitpid(process_queue[current_process].pid, NULL, 0);

        // Shift remaining processes in the queue
        for (int i = current_process; i < process_count - 1; i++) {
            process_queue[i] = process_queue[i + 1];
        }
        process_count--;

        // If all processes finished, stop the timer
        if (process_count == 0) {
            printf("All processes completed.\n");
            timer.it_value.tv_sec = 0;
            timer.it_value.tv_usec = 0;
            setitimer(ITIMER_REAL, &timer, NULL);
            return;
        }

        // Adjust index to avoid out-of-bounds access
        if (current_process >= process_count) {
            current_process = 0;
        }
    }

    // Move to the next process in a circular fashion
    current_process = (current_process + 1) % process_count;

    // Resume the next process
    if (kill(process_queue[current_process].pid, SIGCONT) == 0) {
        printf("Process %d (PID=%d) resumed, remaining time: %d ms\n", 
            current_process + 1, process_queue[current_process].pid, 
            process_queue[current_process].remaining_time);
    }
}

// Function to set up the Round-Robin timer
void setup_timer() {
    struct sigaction sa;
    sa.sa_handler = timer_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;
    sigaction(SIGALRM, &sa, NULL);

    timer.it_value.tv_sec = 0;
    timer.it_value.tv_usec = TIME_QUANTUM * 1000;
    timer.it_interval.tv_sec = 0;
    timer.it_interval.tv_usec = TIME_QUANTUM * 1000;

    setitimer(ITIMER_REAL, &timer, NULL);
}

int main() {
    printf("Starting FIFO Round-Robin Scheduler...\n");

    // Simulating process execution
    for (int i = 0; i < 3; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            // Child process: Simulate work
            printf("Process %d (PID=%d) started\n", i + 1, getpid());
            while (1) pause(); // Wait for signals
            exit(0);
        } else if (pid > 0) {
            // Parent process: Store process info
            process_queue[process_count].pid = pid;
            process_queue[process_count].remaining_time = 3000; // Simulated total runtime
            process_count++;
        } else {
            perror("Fork failed");
            exit(1);
        }
    }

    // Set up Round-Robin scheduling
    setup_timer();

    // Allow the first process to run
    if (process_count > 0) {
        kill(process_queue[0].pid, SIGCONT);
        printf("Process 1 (PID=%d) started first.\n", process_queue[0].pid);
    }

    // Wait for all processes to finish
    while (process_count > 0) {
        pause(); // Wait for timer signals
    }

    printf("All processes completed.\n");
    return 0;
}
