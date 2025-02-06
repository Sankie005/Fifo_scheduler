#!/bin/bash
# install_sched_ext.sh - Script to install the sched_ext kernel extension on Ubuntu

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (e.g., sudo ./install_sched_ext.sh)"
    exit 1
fi

echo "Updating package lists and installing required packages..."
apt-get update
apt-get install -y build-essential linux-headers-$(uname -r) git

# Define the repository URL for sched_ext
REPO_URL="https://github.com/yourusername/sched_ext.git"
INSTALL_DIR="/usr/local/src/sched_ext"

# Clone the sched_ext repository if not already cloned
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Cloning sched_ext repository from $REPO_URL..."
    git clone "$REPO_URL" "$INSTALL_DIR" || { echo "Failed to clone sched_ext repository"; exit 1; }
else
    echo "sched_ext repository already exists at $INSTALL_DIR. Pulling latest changes..."
    cd "$INSTALL_DIR" && git pull || { echo "Failed to update sched_ext repository"; exit 1; }
fi

# Build the sched_ext kernel module
cd "$INSTALL_DIR" || exit 1
echo "Building the sched_ext kernel module..."
make || { echo "Build failed. Ensure the Makefile and source files are correct."; exit 1; }

# Optionally install the module (this example assumes the Makefile supports an 'install' target)
echo "Installing the sched_ext kernel module..."
make install || { echo "Module installation failed."; exit 1; }

# Load the kernel module (check if it is not already loaded)
if ! lsmod | grep -q '^sched_ext'; then
    echo "Loading the sched_ext module..."
    modprobe sched_ext || { echo "Failed to load sched_ext module. Check dmesg for details."; exit 1; }
else
    echo "sched_ext module is already loaded."
fi

echo "sched_ext installation complete."
