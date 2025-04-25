#!/bin/bash
# Simulated malicious actions for sandbox testing (COMPLETED)

# FILE ACCESS
echo "[ACTION: FILE ACCESS]"
cat /etc/shadow

# FILE WRITE
echo "[ACTION: FILE WRITE]"
touch /etc/test_write.txt

# NETWORK ACCESS
echo "[ACTION: NETWORK ACCESS]"
ping -c 1 8.8.8.8

# PRIVILEGE ESCALATION
echo "[ACTION: PRIVILEGE ESCALATION]"
sudo ls /root
