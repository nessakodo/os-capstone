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

def run_command(command, use_firejail=False, command_iterations=300):
    """
    Executes a command with or without Firejail and measures execution time and CPU usage.
    """
    if use_firejail:
        cmd = ["firejail", "--quiet", "--private", "--"] + command
    else:
        cmd = command

    cpu_total = psutil.cpu_percent(interval=None)
    start_time = time.time()


    try:
        for i in range(command_iterations):
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
            success = result.returncode == 0
            error_msg = result.stderr.decode().strip()
            cpu_total += psutil.cpu_percent(interval=None)
    
    except Exception as e:
        success = False
        error_msg = str(e)

    end_time = time.time()


    execution_time = end_time - start_time
    cpu_usage = (cpu_total/command_iterations)

    return execution_time, cpu_usage, success, error_msg

# Execute each command in both environments
print("\n====== FIREJAIL SANDBOXING COMPARISON ======\n")

for cmd in commands:
    cmd_str = ' '.join(cmd)
    print(f"[COMMAND]: {cmd_str}")
    print("-" * 60)

    # Run without Firejail
    direct_time, direct_cpu, direct_success, direct_error = run_command(cmd, use_firejail=False)
    direct_status = "PASS ✅" if direct_success else "FAIL ❌"
    print(f"WITHOUT FIREJAIL")
    print(f"  Time      : {direct_time:.4f}s")
    print(f"  CPU Usage : {direct_cpu:.2f}%")
    print(f"  Status    : {direct_status}")
    if not direct_success:
        print(f"  Error     : {direct_error}")

    print()

    # Run with Firejail
    sandbox_time, sandbox_cpu, sandbox_success, sandbox_error = run_command(cmd, use_firejail=True)
    sandbox_status = "PASS ✅" if sandbox_success else "BLOCKED ❌"
    print(f"WITH FIREJAIL")
    print(f"  Time      : {sandbox_time:.4f}s")
    print(f"  CPU Usage : {sandbox_cpu:.2f}%")
    print(f"  Status    : {sandbox_status}")
    if not sandbox_success:
        print(f"  Error     : {sandbox_error}")

    # Handle edge cases
    if not direct_success and not sandbox_success:
        print("\n[NOTE] Command failed in both environments — may require root or unsupported resource.\n")
    elif direct_cpu == 0 or sandbox_cpu == 0:
        print("\n[NOTE] CPU usage reported as 0% — this often happens for very fast commands. Consider repeating or using heavier workloads.\n")

    # Calculate differences safely
    time_diff = sandbox_time - direct_time
    time_pct = (time_diff / direct_time * 100) if direct_time > 0 else 0
    cpu_diff = sandbox_cpu - direct_cpu
    cpu_pct = (cpu_diff / direct_cpu * 100) if direct_cpu > 0 else 0

    print("OVERHEAD ANALYSIS")
    print(f"  Time Overhead : {time_diff:.4f}s ({time_pct:.2f}%)")
    print(f"  CPU Difference: {cpu_diff:.2f}% ({cpu_pct:.2f}%)")
    print("=" * 60 + "\n")

    # Store results (with fallback to 0.0 if command fails)
    results["command"].append(cmd_str)
    results["sandbox_time"].append(sandbox_time if sandbox_success else 0.0)
    results["direct_time"].append(direct_time if direct_success else 0.0)
    results["time_difference"].append(time_diff)
    results["time_percentage"].append(time_pct)
    results["sandbox_cpu"].append(sandbox_cpu if sandbox_success else 0.0)
    results["direct_cpu"].append(direct_cpu if direct_success else 0.0)
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