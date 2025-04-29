# test.py
# CLI-based sandbox testing script for OS Capstone Project
# Some structure and visualization concepts inspired with help from ChatGPT suggestions,
# refined and customized by team to fit our project requirements.

import subprocess
import sys
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import time
import psutil
import datetime

# ===================================================
# HARDCODED TEST CASES - MODIFY THESE TO TEST DIFFERENT SCENARIOS
# ===================================================
EXAMPLE_COMMANDS = [
    ["ls", "/"],                    # Safe command
    ["ping", "-c", "1", "8.8.8.8"], # Network command
    ["touch", "/etc/testfile"],     # Should be blocked
    ["cat", "/etc/passwd"],         # Should be blocked
    ["whoami"],                     # Safe command
    ["echo", "Hello World"],        # Safe command
]

# ===================================================
# CPU UTILIZATION TRACKING
# ===================================================
def get_cpu_utilization(duration=1):
    """Get average CPU utilization over a duration in seconds"""
    start_time = time.time()
    cpu_percentages = []
    
    while time.time() - start_time < duration:
        cpu_percentages.append(psutil.cpu_percent(interval=0.1))
    
    return sum(cpu_percentages) / len(cpu_percentages) if cpu_percentages else 0

def check_command_safety(command):
    """Runs a command inside Firejail and returns True if it succeeds, False if blocked."""
    # firejail_command = ["firejail", "--quiet", "--noprofile", *command]
    firejail_command = ["firejail", "--private", "--quiet", "--"] + cmd # UPDATED

    try:
        result = subprocess.run(firejail_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        output = result.stdout.decode()
        error = result.stderr.decode()

        # Interpret non-critical firejail warnings as okay
        if "error" in error.lower() or result.returncode != 0:
            print(f"[!] Command '{' '.join(command)}' may not be safe.")
            print(f"[stderr]: {error.strip()}")
            return False
        else:
            print(f"[✓] Command '{' '.join(command)}' appears safe.")
            print(f"[stdout]: {output.strip()}")
            return True

    except Exception as e:
        print(f"[x] Error during sandbox check: {str(e)}")
        return False
    

def time_command_execution(command, use_sandbox=True):
    """
    Executes a command with or without sandbox and measures execution time and CPU usage.
    Returns execution time in seconds, CPU utilization, and result status.
    """
    start_time = time.time()
    
    if use_sandbox:
        cmd = ["firejail", "--quiet", "--noprofile", *command]
    else:
        cmd = command
    
    try:
        # Get CPU utilization before command
        cpu_before = get_cpu_utilization(0.5)
        
        # Run the command
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        
        # Get CPU utilization after command
        cpu_after = get_cpu_utilization(0.5)
        
        execution_time = time.time() - start_time
        success = result.returncode == 0
        return execution_time, (cpu_before, cpu_after), success, result
    except Exception as e:
        execution_time = time.time() - start_time
        return execution_time, (0, 0), False, None
    
# Adding placeholder for plotting (Killian's implementation to be merged here)

# simple bar chart example
# def visualize_results(results):
#     """Creates a simple bar chart showing safe vs unsafe commands."""
#     labels = ['Safe', 'Unsafe']
#     values = [results['safe'], results['unsafe']]

#     plt.bar(labels, values, color=['green', 'red'])
#     plt.title('Sandboxed Command Safety Results')
#     plt.ylabel('Number of Commands')
#     plt.tight_layout()
#     plt.savefig('visuals/test_summary.png')
#     plt.show()

# fancy color custom bar chart example
def visualize_results(results):
    """Plot Safe vs Unsafe command results as a clean bar chart."""
    os.makedirs('visuals', exist_ok=True)

    labels = ['Safe', 'Unsafe']
    counts = [results['safe'], results['unsafe']]
    colors = ['#4CAF50', '#FF6B6B']  # softer green and coral red

    fig, ax = plt.subplots()
    ax.bar(labels, counts, color=colors, edgecolor='black', linewidth=1.2)

    # Add value labels on top of bars
    for i, v in enumerate(counts):
        ax.text(i, v + 0.2, str(v), ha='center', va='bottom', fontsize=10, weight='bold')

    ax.set_title('Sandboxed Command Safety', fontsize=16, weight='bold')
    ax.set_ylabel('Number of Commands')
    ax.set_facecolor('#f9f9f9')  # softer background
    fig.tight_layout()

    plt.savefig('visuals/test_summary.png')
    plt.close()

def visualize_performance(performance_results):
    """Create a bar chart comparing sandbox vs direct execution times"""
    if not performance_results["command"]:
        print("No performance data to visualize.")
        return
    
    os.makedirs('visuals', exist_ok=True)
    
    # Create figure with appropriate size
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set up bar positions
    commands = performance_results["command"]
    x = range(len(commands))
    width = 0.35
    
    # Create bars
    sandbox_bars = ax.bar([i - width/2 for i in x], performance_results["sandbox_time"], 
                         width, label='With Sandbox', color='#4CAF50', edgecolor='black')
    direct_bars = ax.bar([i + width/2 for i in x], performance_results["direct_time"], 
                        width, label='Without Sandbox', color='#2196F3', edgecolor='black')
    
    # Add labels and title
    ax.set_xlabel('Commands')
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Performance Impact of Sandboxing', fontsize=16, weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(commands, rotation=45, ha='right')
    ax.legend()
    
    # Add value labels on top of bars
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.4f}s',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

    add_labels(sandbox_bars)
    add_labels(direct_bars)

    # Add a second plot for percentage overhead
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    percentage_bars = ax2.bar(commands, performance_results["time_percentage"], 
                                color='#FF9800', edgecolor='black')

    ax2.set_xlabel('Commands')
    ax2.set_ylabel('Overhead Percentage (%)')
    ax2.set_title('Percentage Overhead of Sandboxing', fontsize=16, weight='bold')
    ax2.set_xticklabels(commands, rotation=45, ha='right')

    # Add value labels for percentage bars
    for bar in percentage_bars:
        height = bar.get_height()
        ax2.annotate(f'{height:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

    fig.tight_layout()
    fig2.tight_layout()

    # Save plots
    plt.savefig('visuals/execution_time_comparison.png')
    plt.close(fig)
    plt.savefig('visuals/sandbox_overhead_percentage.png')
    plt.close(fig2)

def visualize_cpu_usage(performance_results):
    """Create a bar chart showing CPU utilization before and after commands"""
    if not performance_results["command"]:
        print("No CPU data to visualize.")
        return
    
    os.makedirs('visuals', exist_ok=True)
    
    commands = performance_results["command"]
    cpu_before = performance_results["cpu_before"]
    cpu_after = performance_results["cpu_after"]
    
    x = range(len(commands))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    before_bars = ax.bar([i - width/2 for i in x], cpu_before, width, 
                        label='Before Command', color='#4CAF50')
    after_bars = ax.bar([i + width/2 for i in x], cpu_after, width, 
                       label='After Command', color='#2196F3')
    
    ax.set_xlabel('Commands')
    ax.set_ylabel('CPU Utilization (%)')
    ax.set_title('CPU Usage Before and After Command Execution', fontsize=16, weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(commands, rotation=45, ha='right')
    ax.legend()
    
    # Add value labels
    for bars in [before_bars, after_bars]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('visuals/cpu_usage_comparison.png')
    plt.close()

if __name__ == "__main__":
    print("\n[HARDCODED MODE]: Running Example Attack Simulations ⚡\n")
    
    results = {"safe": 0, "unsafe": 0}
    performance_results = {
        "command": [],
        "sandbox_time": [],
        "direct_time": [],
        "time_difference": [],
        "time_percentage": [],
        "cpu_before": [],
        "cpu_after": []
    }

    for cmd in EXAMPLE_COMMANDS:
        print(f"\n[TESTING]: {' '.join(cmd)}")
        
        # Test with sandbox
        sandbox_time, (cpu_before, cpu_after), sandbox_success, sandbox_result = time_command_execution(cmd, use_sandbox=True)
        print(f"   -> Sandbox execution: {'SUCCESS' if sandbox_success else 'FAILED'} (Time: {sandbox_time:.4f}s)")
        print(f"   -> CPU Usage: {cpu_before:.1f}% -> {cpu_after:.1f}%")
        
        # Only test without sandbox if the command is safe
        if sandbox_success:
            direct_time, _, direct_success, _ = time_command_execution(cmd, use_sandbox=False)
            print(f"   -> Direct execution: {'SUCCESS' if direct_success else 'FAILED'} (Time: {direct_time:.4f}s)")
            
            time_diff = sandbox_time - direct_time
            percentage = (time_diff / direct_time) * 100 if direct_time > 0 else 0
            
            print(f"   -> Sandbox overhead: {time_diff:.4f}s ({percentage:.2f}%)")
            
            # Store results
            performance_results["command"].append(' '.join(cmd))
            performance_results["sandbox_time"].append(sandbox_time)
            performance_results["direct_time"].append(direct_time)
            performance_results["time_difference"].append(time_diff)
            performance_results["time_percentage"].append(percentage)
            performance_results["cpu_before"].append(cpu_before)
            performance_results["cpu_after"].append(cpu_after)
        else:
            print("   -> Direct execution: SKIPPED (unsafe command)")
        
        # Update safe/unsafe counts
        if sandbox_success:
            results['safe'] += 1
            print("   -> Result: SAFE ✅")
        else:
            results['unsafe'] += 1
            print("   -> Result: BLOCKED/UNSAFE ❌")

    # Generate all visualizations
    visualize_results(results)
    visualize_performance(performance_results)
    visualize_cpu_usage(performance_results)
    
    print("\nVisualizations have been saved to the 'visuals' directory:")
    print("1. test_summary.png - Shows safe vs unsafe commands")
    print("2. execution_time_comparison.png - Shows execution time with/without sandbox")
    print("3. sandbox_overhead_percentage.png - Shows percentage overhead")
    print("4. cpu_usage_comparison.png - Shows CPU usage before/after commands")
