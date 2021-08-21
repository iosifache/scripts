#!/bin/bash

# Copy the script and the configuration
mkdir /opt/checkmk_alert
cp -r * /opt/checkmk_alert

# Create a new crontab
(crontab -l 2>/dev/null; echo "*/5 * * * *\
 /opt/checkmk_alert/checkmk_alert.py &>/opt/checkmk_alert/log.txt")\
 | crontab -