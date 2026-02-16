#!/bin/bash
# ARGUS Linux Installer
# "The All-Seeing Network Eye"

echo "👁️  Installing ARGUS Dependencies..."

# 1. System Dependencies (libpcap for Scapy)
if [ -x "$(command -v apt-get)" ]; then
    sudo apt-get update
    sudo apt-get install -y python3-pip libpcap-dev
elif [ -x "$(command -v yum)" ]; then
    sudo yum install -y python3-pip libpcap-devel
fi

# 2. Python Dependencies
pip3 install -r requirements.txt

# 3. Permissions (Raw Sockets need root)
echo "🔒 Setting capabilities for raw socket access..."
# This allows python to sniff without being fully root
sudo setcap cap_net_raw=eip $(readlink -f $(which python3)) 2>/dev/null || echo "⚠️  Could not set capabilities. You may need to run as sudo."

echo "✅ Installation Complete."
echo "   Run: sudo python3 project_alpha/main.py --train"
