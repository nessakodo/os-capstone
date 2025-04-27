# attack_scenarios.py
# Simulated attack attempts for OS Capstone Project, based on GPT-generated scaffolding

import os
import subprocess
from datetime import datetime

RESULTS_DIR = "./results"

def log_result(filename, action, result, error=None):
    """Log the result of an action to a file with timestamps."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, filename), "a") as f:
        f.write(f"[{timestamp}] ACTION: {action}\n")
        f.write(f"RESULT: {result}\n")
        if error:
            f.write(f"ERROR: {error}\n")
        f.write("-" * 40 + "\n")

def simulate_file_access():
    action = "Read /etc/shadow and write to /tmp/stolen_shadow.txt"
    try:
        with open("/etc/shadow", "r") as f:
            data = f.read()
        with open("/tmp/stolen_shadow.txt", "w") as out:
            out.write(data)
        log_result("file_access.log", action, "SUCCESS")
    except Exception as e:
        log_result("file_access.log", action, "FAILED", str(e))

def simulate_network_access():
    action = "Curl example.com and write to /tmp/network_test.html"
    try:
        subprocess.run(
            ["curl", "-s", "http://example.com", "-o", "/tmp/network_test.html"],
            check=True,
            stderr=subprocess.PIPE
        )
        log_result("network_access.log", action, "SUCCESS")
    except subprocess.CalledProcessError as e:
        log_result("network_access.log", action, "FAILED", e.stderr.decode().strip())

def simulate_privilege_escalation():
    action = "Touch file in /root (requires sudo)"
    try:
        subprocess.run(
            ["sudo", "touch", "/root/hacked.txt"],
            check=True,
            stderr=subprocess.PIPE
        )
        log_result("privilege_escalation.log", action, "SUCCESS")
    except subprocess.CalledProcessError as e:
        log_result("privilege_escalation.log", action, "FAILED", e.stderr.decode().strip())

if __name__ == "__main__":
    simulate_file_access()
    simulate_network_access()
    simulate_privilege_escalation()
