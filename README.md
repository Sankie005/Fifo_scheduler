# LIFO and FIFO Schedulers using Sched_ext 
*** 
### Usage
#### Installation
[Install Sched_ext using the provided install script or follow the guide](https://github.com/sched-ext/scx?tab=readme-ov-file#install-instructions-by-distro)
To use provided script:
`chmod +x install_sched_ext.sh`
`sudo ./install_sched_ext.sh`
### Deploying
`chmod +x deploy.sh`
`sudo ./deploy.sh`

After this step you should hopefully see two log files named `fifo_scheduler.log` and `lifo_scheduler.log`

### Running python graphing step 
1. Create a new venv with `python3 -m venv venv` you may have to install python3 virtual environments if it doesn't come pre installed, here's a link to a [guide](https://www.arubacloud.com/tutorial/how-to-create-a-python-virtual-environment-on-ubuntu.aspx)
2. Actvate the virtual environment with `source nameofyourvenv/bin/activate`
3. Install matplotlib with `pip install maptlotlib`
4. Run the script with `python3 plot_fifo.py`

# Output 
The output should be stored in schedulers_gnatt.png 
Additional support may be needed to display png files depending on your linux distribution. 

## Understanding the scheduling 
***
All schedulers currently "simulate" 3 child processes by simply sleeping for 3seconds each, we then also stagger their deployment by a 100ms to make the data easier to understand and work with. 
Additional code is present to create and lock the log files while the schedulers are running to prevent them being overwritten or malformed. 
### FIFO Scheduler:
Follows the "First In First Out" principle, the processes are simply presented in the order that they arrive. 

### LIFO Scheduler: 
Implments "Last In First Out" principle by increasing the priority of processes as they are added to the queue, resulting in processes that arrive at the end to have a higher priority. 
![Chart](https://github.com/Sankie005/Fifo_scheduler/blob/main/schedulers_gantt.png?raw=true)