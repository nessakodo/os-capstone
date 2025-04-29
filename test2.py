import subprocess
import time
import csv
import psutil
import matplotlib.pyplot as plt

# List of commands to test
commands = [
    "ls /root",
    "ping -c 1 google.com",
    "mkdir /etc/testdir",
    "touch ~/firejail_testfile",
    "whoami"
]

# File to store results
csv_file = "firejail_test_results.csv"

# Run a command and measure execution time and CPU usage
def run_command(cmd, use_firejail=False):
    if use_firejail:
        full_cmd = ["firejail", "--private", "--quiet", "--"] + cmd.split()
    else:
        full_cmd = cmd.split()

    cpu_before = psutil.cpu_percent(interval=None)
    start_time = time.time()

    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=10)
        success = (result.returncode == 0)
        stderr = result.stderr.strip()
    except Exception as e:
        success = False
        stderr = str(e)

    end_time = time.time()
    cpu_after = psutil.cpu_percent(interval=None)
    cpu_usage = cpu_after - cpu_before
    execution_time = end_time - start_time

    return {
        "command": cmd,
        "sandboxed": use_firejail,
        "success": success,
        "execution_time": execution_time,
        "cpu_usage": cpu_usage,
        "stderr": stderr
    }

# Run all commands normally and with Firejail
results = []

for cmd in commands:
    results.append(run_command(cmd, use_firejail=False))
    results.append(run_command(cmd, use_firejail=True))

# Write results to CSV
with open(csv_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

# Visualize CPU Usage
sandboxed_cpu = [r['cpu_usage'] for r in results if r['sandboxed']]
normal_cpu = [r['cpu_usage'] for r in results if not r['sandboxed']]
labels = [r['command'] for r in results if not r['sandboxed']]

x = range(len(labels))

plt.figure(figsize=(10, 6))
plt.bar(x, normal_cpu, width=0.4, label="Normal", align="center")
plt.bar(x, sandboxed_cpu, width=0.4, label="Firejail (Private)", align="edge")
plt.xlabel("Command")
plt.ylabel("CPU Usage (%)")
plt.title("CPU Usage Comparison: Normal vs Firejail")
plt.xticks(x, labels, rotation=45, ha="right")
plt.legend()
plt.tight_layout()
plt.show()