import matplotlib.pyplot as plt
import re

def parse_fifo_log(log_text):
    processes = {}
    
    for line in log_text.split('\n'):
        if not line or "All child processes" in line:
            continue
            
        # Extract process information
        match = re.search(r'Process (\d+) \(PID=(\d+)\) (starting|finished) work at (\d+)', line)
        if not match:
            continue
            
        process_num, pid, action, timestamp = match.groups()
        timestamp = int(timestamp)
        
        if pid not in processes:
            processes[pid] = {
                'intervals': [],
                'number': process_num,
                'start_time': timestamp
            }
            
        if action == 'starting':
            processes[pid]['intervals'].append([timestamp, None])
        elif action == 'finished':
            if processes[pid]['intervals'] and processes[pid]['intervals'][-1][1] is None:
                processes[pid]['intervals'][-1][1] = timestamp
                
    return processes, min(p['start_time'] for p in processes.values())

def parse_lifo_log(log_text):
    processes = {}
    
    for line in log_text.split('\n'):
        if not line or "All child processes" in line or "is working" in line:
            continue
            
        # Extract process information
        match = re.search(r'Process (\d+) \(PID (\d+)\) (starting|finished) work(?: with priority \d+)? at (\d+)', line)
        if not match:
            continue
            
        process_num, pid, action, timestamp = match.groups()
        timestamp = int(timestamp)
        
        if pid not in processes:
            processes[pid] = {
                'intervals': [],
                'number': process_num,
                'start_time': timestamp
            }
            
        if action == 'starting':
            processes[pid]['intervals'].append([timestamp, None])
        elif action == 'finished':
            if processes[pid]['intervals'] and processes[pid]['intervals'][-1][1] is None:
                processes[pid]['intervals'][-1][1] = timestamp
                
    return processes, min(p['start_time'] for p in processes.values())

def parse_fifo_rr_log(log_text):
    processes = {}
    current_time = 0
    time_quantum = 100
    
    for line in log_text.split('\n'):
        if not line or "Starting" in line:
            continue
            
        if "All processes completed" in line:
            for process_data in processes.values():
                if process_data['intervals'] and process_data['intervals'][-1][1] is None:
                    process_data['intervals'][-1][1] = current_time + time_quantum
            continue
            
        pid_match = re.search(r'Process (\d+) \(PID=(\d+)\)', line)
        if not pid_match:
            continue
            
        process_num = pid_match.group(1)
        pid = pid_match.group(2)
        
        if pid not in processes:
            processes[pid] = {
                'intervals': [],
                'start_time': current_time,
                'number': process_num
            }
        
        if "started" in line or "resumed" in line:
            processes[pid]['intervals'].append([current_time, None])
        elif "paused" in line or "finished" in line:
            if processes[pid]['intervals'][-1][1] is None:
                processes[pid]['intervals'][-1][1] = current_time + time_quantum
            current_time += time_quantum
            
    return processes, 0

def create_combined_gantt_chart(all_processes_data):
    # Create figure with three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))
    colors = ['#FF9999', '#99FF99', '#9999FF']
    
    # Plot each scheduler type
    for (processes, base_time, title, ax) in [
        (all_processes_data['fifo'], all_processes_data['fifo_base'], 'FIFO Scheduler', ax1),
        (all_processes_data['lifo'], all_processes_data['lifo_base'], 'LIFO Scheduler', ax2),
        (all_processes_data['fifo_rr'], all_processes_data['fifo_rr_base'], 'FIFO Round-Robin Scheduler', ax3)
    ]:
        # Plot processes for this scheduler
        for i, (pid, data) in enumerate(processes.items()):
            process_label = f'Process {data["number"]}'
            
            for start, end in data['intervals']:
                # Normalize times relative to the base_time
                normalized_start = (start - base_time) / 1000  # Convert to seconds
                normalized_end = (end - base_time) / 1000
                
                ax.barh(i, normalized_end - normalized_start, 
                       left=normalized_start, height=0.3,
                       color=colors[i % len(colors)],
                       edgecolor='black',
                       label=process_label if start == data['intervals'][0][0] else "")
        
        # Customize each subplot
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Processes')
        ax.set_title(title)
        ax.set_yticks(range(len(processes)))
        ax.set_yticklabels([f'Process {data["number"]}' for pid, data in processes.items()])
        ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        ax.legend()
    
    plt.tight_layout()
    return fig

def plot_all_schedulers():
    # Read and parse all log files
    with open('fifo_scheduler.log', 'r') as f:
        fifo_processes, fifo_base = parse_fifo_log(f.read())
    
    with open('lifo_scheduler.log', 'r') as f:
        lifo_processes, lifo_base = parse_lifo_log(f.read())
    
    with open('fifo_rr_scheduler.log', 'r') as f:
        fifo_rr_processes, fifo_rr_base = parse_fifo_rr_log(f.read())
    
    # Combine all data
    all_processes_data = {
        'fifo': fifo_processes,
        'fifo_base': fifo_base,
        'lifo': lifo_processes,
        'lifo_base': lifo_base,
        'fifo_rr': fifo_rr_processes,
        'fifo_rr_base': fifo_rr_base
    }
    
    # Create and save the combined chart
    fig = create_combined_gantt_chart(all_processes_data)
    plt.savefig('schedulers_gantt.png', dpi=300, bbox_inches='tight')
    plt.close()

# Run the combined visualization
plot_all_schedulers()