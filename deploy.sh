#!/bin/bash
# deploy.sh - Compile and run the FIFO scheduler

# Ensure the script is run as root (or via sudo)
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (e.g., using sudo)"
    exit 1
fi

echo "Cleaning and compiling the FIFO scheduler..."
make clean
make

echo "Running the FIFO scheduler..."
./fifo_scheduler

echo "Execution complete. Check the log file: fifo_scheduler.log"
