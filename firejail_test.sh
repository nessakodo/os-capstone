#!/bin/bash
# Checking Firejail installation and running a basic sandboxed command (COMPLETED)

echo "[TEST] Checking Firejail installation..."
command -v firejail > /dev/null || { echo "Firejail is NOT installed."; exit 1; }
echo "Firejail is installed."


echo "[TEST] Running ls / inside Firejail..."
firejail --quiet -- ls /
