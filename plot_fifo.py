#!/usr/bin/env python3
"""
plot_fifo.py - Parse fifo_scheduler.log and plot a Gantt chart of process execution.

Expected log file format (one line per process):
PID=1234, start=16000, end=19000
"""

import matplotlib.pyplot as plt

def parse_log(log_file):
    processes = []
    with open(log_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(',')
                pid_str = parts[0].split('=')[1].strip()
                start_str = parts[1].split('=')[1].strip()
                end_str = parts[2].split('=')[1].strip()
                pid = int(pid_str)
                start = int(start_str)
                end = int(end_str)
                processes.append((pid, start, end))
    return processes

def plot_gantt(processes):
    # Sort processes by start time
    processes.sort(key=lambda x: x[1])
    # Normalize times relative to the earliest start time
    min_start = min(p[1] for p in processes)
    normalized = [(pid, start - min_start, end - min_start) for (pid, start, end) in processes]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    yticks = []
    yticklabels = []
    for i, (pid, start, end) in enumerate(normalized):
        duration = end - start
        ax.broken_barh([(start, duration)], (i*10, 9), facecolors='tab:blue')
        yticks.append(i*10 + 4.5)
        yticklabels.append(f"PID {pid}")
    
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Processes")
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_title("FIFO Scheduler Process Execution Timeline")
    plt.tight_layout()
    plt.savefig("fifo_scheduler_gantt.png")
    print("Gantt chart saved to fifo_scheduler_gantt.png")


def main():
    log_file = "fifo_scheduler.log"
    processes = parse_log(log_file)
    if not processes:
        print("No process data found in log file.")
        return
    plot_gantt(processes)

if __name__ == '__main__':
    main()
