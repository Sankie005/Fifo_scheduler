#!/bin/bash
# deploy.sh - Compile and run the selected scheduler(s)
# Options:
#   1) FIFO Scheduler
#   2) LIFO Scheduler
#   3) Round-Robin FIFO Scheduler
#   4) All (FIFO, LIFO, then Round-Robin FIFO consecutively)

# Ensure the script is run as root (or via sudo)
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (e.g., using sudo)"
    exit 1
fi

echo "Select the scheduler to deploy:"
echo "1) FIFO Scheduler"
echo "2) LIFO Scheduler"
echo "3) Round-Robin FIFO Scheduler"
echo "4) All (FIFO, LIFO, then Round-Robin FIFO consecutively)"
read -p "Enter your choice (1, 2, 3, or 4): " choice

# Clean build environment
echo "Cleaning previous builds..."
make clean

case "$choice" in
    1)
        echo "Compiling FIFO scheduler..."
        make fifo_scheduler || { echo "Compilation failed for FIFO scheduler"; exit 1; }
        echo "Running FIFO scheduler..."
        ./fifo_scheduler > fifo_scheduler.log 2>&1 || { echo "Execution failed for FIFO scheduler"; exit 1; }
        echo "FIFO scheduler execution complete. Check fifo_scheduler.log."
        ;;
    2)
        echo "Compiling LIFO scheduler..."
        make lifo_scheduler || { echo "Compilation failed for LIFO scheduler"; exit 1; }
        echo "Running LIFO scheduler..."
        ./lifo_scheduler > lifo_scheduler.log 2>&1 || { echo "Execution failed for LIFO scheduler"; exit 1; }
        echo "LIFO scheduler execution complete. Check lifo_scheduler.log."
        ;;
    3)
        echo "Compiling Round-Robin FIFO scheduler..."
        make fifo_rr_scheduler || { echo "Compilation failed for Round-Robin FIFO scheduler"; exit 1; }
        echo "Running Round-Robin FIFO scheduler..."
        ./fifo_rr_scheduler > fifo_rr_scheduler.log 2>&1 || { echo "Execution failed for Round-Robin FIFO scheduler"; exit 1; }
        echo "Round-Robin FIFO scheduler execution complete. Check fifo_rr_scheduler.log."
        ;;
    4)
        echo "Compiling all schedulers..."
        make fifo_scheduler lifo_scheduler fifo_rr_scheduler || { echo "Compilation failed"; exit 1; }
        
        echo "Running FIFO scheduler..."
        ./fifo_scheduler > fifo_scheduler.log 2>&1 || { echo "Execution failed for FIFO scheduler"; exit 1; }
        echo "FIFO scheduler execution complete. Check fifo_scheduler.log."
        
        echo "Running LIFO scheduler..."
        ./lifo_scheduler > lifo_scheduler.log 2>&1 || { echo "Execution failed for LIFO scheduler"; exit 1; }
        echo "LIFO scheduler execution complete. Check lifo_scheduler.log."
        
        echo "Running Round-Robin FIFO scheduler..."
        ./fifo_rr_scheduler > fifo_rr_scheduler.log 2>&1 || { echo "Execution failed for Round-Robin FIFO scheduler"; exit 1; }
        echo "Round-Robin FIFO scheduler execution complete. Check fifo_rr_scheduler.log."
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo "Deployment complete."
