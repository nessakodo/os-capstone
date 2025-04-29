import subprocess
import time
import psutil
import matplotlib.pyplot as plt
import os

# Define the list of commands to test
commands = [
    ["ls", "/root"],
    ["ping", "-c", "1", "8.8.8.8"],
    ["mkdir", "/etc/testdir"],
    ["touch", "/tmp/firejail_testfile"],
    ["whoami"]
]

# Initialize result storage
results = {
    "command": [],
    "sandbox_time": [],
    "direct_time": [],
    "time_difference": [],
    "time_percentage": [],
    "sandbox_cpu": [],
    "direct_cpu": [],
    "cpu_difference": [],
    "cpu_percentage": []
}

def run_command(command, use_firejail=False):
    """
    Executes a command with or without Firejail and measures execution time and CPU usage.
    """
    if use_firejail:
        cmd = ["firejail", "--quiet", "--private", "--"] + command
    else:
        cmd = command

    # Record CPU usage before execution
    cpu_before = psutil.cpu_percent(interval=None)

    start_time = time.time()
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        success = True
    except Exception as e:
        success = False
    end_time = time.time()

    # Record CPU usage after execution
    cpu_after = psutil.cpu_percent(interval=None)

    execution_time = end_time - start_time
    cpu_usage = cpu_after - cpu_before

    return execution_time, cpu_usage, success

# Execute each command in both environments
for cmd in commands:
    cmd_str = ' '.join(cmd)
    print(f"Testing command: {cmd_str}")

    # Run without Firejail
    direct_time, direct_cpu, direct_success = run_command(cmd, use_firejail=False)
    print(f"  Without Firejail - Time: {direct_time:.4f}s, CPU: {direct_cpu:.2f}%")

    # Run with Firejail
    sandbox_time, sandbox_cpu, sandbox_success = run_command(cmd, use_firejail=True)
    print(f"  With Firejail    - Time: {sandbox_time:.4f}s, CPU: {sandbox_cpu:.2f}%")

    # Calculate differences
    time_diff = sandbox_time - direct_time
    cpu_diff = sandbox_cpu - direct_cpu
    time_pct = (time_diff / direct_time * 100) if direct_time > 0 else 0
    cpu_pct = (cpu_diff / direct_cpu * 100) if direct_cpu > 0 else 0

    # Store results
    results["command"].append(cmd_str)
    results["sandbox_time"].append(sandbox_time)
    results["direct_time"].append(direct_time)
    results["time_difference"].append(time_diff)
    results["time_percentage"].append(time_pct)
    results["sandbox_cpu"].append(sandbox_cpu)
    results["direct_cpu"].append(direct_cpu)
    results["cpu_difference"].append(cpu_diff)
    results["cpu_percentage"].append(cpu_pct)

# Create output directory for visuals
os.makedirs('visuals', exist_ok=True)

# Visualization 1: Execution Time Comparison
plt.figure(figsize=(10, 6))
x = range(len(results["command"]))
plt.bar([i - 0.2 for i in x], results["direct_time"], width=0.4, label='Without Firejail', color='skyblue')
plt.bar([i + 0.2 for i in x], results["sandbox_time"], width=0.4, label='With Firejail', color='salmon')
plt.xticks(x, results["command"], rotation=45, ha='right')
plt.ylabel('Execution Time (s)')
plt.title('Execution Time Comparison')
plt.legend()
plt.tight_layout()
plt.savefig('visuals/execution_time_comparison.png')
plt.show()

# Visualization 2: CPU Utilization Comparison
plt.figure(figsize=(10, 6))
plt.bar([i - 0.2 for i in x], results["direct_cpu"], width=0.4, label='Without Firejail', color='lightgreen')
plt.bar([i + 0.2 for i in x], results["sandbox_cpu"], width=0.4, label='With Firejail', color='orange')
plt.xticks(x, results["command"], rotation=45, ha='right')
plt.ylabel('CPU Utilization (%)')
plt.title('CPU Utilization Comparison')
plt.legend()
plt.tight_layout()
plt.savefig('visuals/cpu_utilization_comparison.png')
plt.show()

# Visualization 3: Sandbox Overhead Percentage
plt.figure(figsize=(10, 6))
plt.bar(x, results["time_percentage"], color='purple')
plt.xticks(x, results["command"], rotation=45, ha='right')
plt.ylabel('Overhead (%)')
plt.title('Sandbox Overhead Percentage')
plt.tight_layout()
plt.savefig('visuals/sandbox_overhead_percentage.png')
plt.show()