#!/bin/bash
set -e
export HIDDENSERVICES=$(getent hosts hiddenservices | awk '{print $1}')
export TORCLIENT=$(getent hosts torclient | awk '{print $1}')
export REDIS=$(getent hosts redis | awk '{print $1}')
echo "socks5 $TORCLIENT 9050" >> /etc/proxychains.conf
python3 /mitm/init_root.py
proxychains4 mitmdump -s /mitm/mitm.py
