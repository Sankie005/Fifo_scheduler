#!/usr/bin/env python3
"""
plot_schedulers.py - Parse fifo_scheduler.log and lifo_scheduler.log and plot Gantt charts
for process execution for both schedulers.

Expected log file format (one line per process):
PID=1234, start=16000, end=19000
"""

import os
import matplotlib.pyplot as plt

def parse_log(log_file):
    """Parse a log file and return a list of tuples (pid, start, end)."""
    processes = []
    try:
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
    except FileNotFoundError:
        print(f"Log file '{log_file}' not found.")
    return processes

def plot_gantt(ax, processes, title):
    """
    Plot a Gantt chart on the given axes for the provided process data.
    
    :param ax: A matplotlib Axes object.
    :param processes: A list of tuples (pid, start, end).
    :param title: Title for the subplot.
    """
    if not processes:
        ax.text(0.5, 0.5, "No data", ha='center', va='center')
        ax.set_title(title)
        return

    # Sort processes by start time and normalize times
    processes.sort(key=lambda x: x[1])
    min_start = min(p[1] for p in processes)
    normalized = [(pid, start - min_start, end - min_start) for (pid, start, end) in processes]

    yticks = []
    yticklabels = []
    for i, (pid, start, end) in enumerate(normalized):
        duration = end - start
        ax.broken_barh([(start, duration)], (i * 10, 9), facecolors='tab:blue')
        yticks.append(i * 10 + 4.5)
        yticklabels.append(f"PID {pid}")

    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Processes")
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_title(title)

def main():
    fifo_log = "fifo_scheduler.log"
    lifo_log = "lifo_scheduler.log"

    fifo_processes = parse_log(fifo_log)
    lifo_processes = parse_log(lifo_log)

    # Create a figure with two subplots (one for each scheduler)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    plot_gantt(ax1, fifo_processes, "FIFO Scheduler Process Execution Timeline")
    plot_gantt(ax2, lifo_processes, "LIFO Scheduler Process Execution Timeline")

    plt.tight_layout()
    output_file = "schedulers_gantt.png"
    plt.savefig(output_file)
    print(f"Gantt charts saved to {output_file}")
    # plt.show() disabled as it doesn't work with non-interactive mode 

if __name__ == '__main__':
    main()
