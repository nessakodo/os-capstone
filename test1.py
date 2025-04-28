# test.py
# CLI-based sandbox testing script for OS Capstone Project
# Some structure and visualization concepts inspired with help from ChatGPT suggestions,
# refined and customized by team to fit our project requirements.

import subprocess
import sys
import os
import matplotlib.pyplot as plt # added for plotting
import time
import psutil
import datetime




def check_command_safety(command):
    """Runs a command inside Firejail and returns True if it succeeds, False if blocked."""
    firejail_command = ["firejail", "--quiet", "--noprofile", *command]

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
    Executes a command with or without sandbox and measures execution time.
    Returns execution time in seconds and result status.
    """
    start_time = time.time()
    
    if use_sandbox:
        # Run with Firejail
        cmd = ["firejail", "--quiet", "--noprofile", *command]
    else:
        # Run directly without sandbox
        cmd = command
    
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        execution_time = time.time() - start_time
        success = result.returncode == 0
        return execution_time, success, result
    except Exception as e:
        execution_time = time.time() - start_time
        return execution_time, False, None
    
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
    plt.show()

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
    fig.savefig('visuals/execution_time_comparison.png')
    fig2.savefig('visuals/sandbox_overhead_percentage.png')
    
    plt.show()

if __name__ == "__main__":

    
    if len(sys.argv) < 2:
        print("\n[HARDCODED MODE]: NO USER INPUT DETECTED - Running Example Attack Simulations ⚡\n") # temporary placeholder

        print("[!] No command provided.") # updated to print when no command
        print("Usage: python3 test.py <command> [arguments]") # shows how the script should be used
        # print("Usage: python check_command_safety.py <command> [arguments]") # original print from Mohammad

        # If no CLI command passed, fallback to example commands
        results = {"safe": 0, "unsafe": 0}

        # Adding placeholder for example commands
        example_commands = [
            ["cat", "/etc/shadow"],
            ["touch", "/etc/testfile"],
            ["ping", "-c", "1", "8.8.8.8"],
            ["sudo", "ls", "/root"]
        ]

        for cmd in example_commands:
            print(f"[TESTING]: {' '.join(cmd)}")
            if check_command_safety(cmd):
                results['safe'] += 1
                print("   -> Result: SAFE ✅\n") # added for style
            else:
                results['unsafe'] += 1 
                print("   -> Result: BLOCKED/UNSAFE ❌\n") # added for style

            # Print summary (added for demo)
            print("================= SUMMARY =================")
            print(f"Safe Commands: {results['safe']} | Unsafe Commands: {results['unsafe']}")
            print(f"Saved results to 'visuals/test_summary.png'")
            print("===========================================\n")


        visualize_results(results) # Idea for visualizing results here from test.py (Killian's implementation to be merged here)

        # sys.exit(1) # from original code to exit the script (can add back but commented out for now)
    else:
         # If user gives a command, only run that command and exit (no graph)
        command = sys.argv[1:]
        if check_command_safety(command):
            print("-> Executing command inside firejail...")
            subprocess.run(["firejail", "--noprofile", *command])
        else:
            print("-> Command execution blocked.")


    # In the main execution block where you run example commands
performance_results = {"command": [], "sandbox_time": [], "direct_time": [], "time_difference": [], "time_percentage": []}

for cmd in example_commands:
    print(f"\n[TESTING]: {' '.join(cmd)}")
    
    # Test with sandbox
    sandbox_time, sandbox_success, sandbox_result = time_command_execution(cmd, use_sandbox=True)
    print(f"   -> Sandbox execution: {'SUCCESS' if sandbox_success else 'FAILED'} (Time: {sandbox_time:.4f}s)")
    
    # Only test without sandbox if the command is safe (to avoid security issues)
    if sandbox_success:
        direct_time, direct_success, direct_result = time_command_execution(cmd, use_sandbox=False)
        print(f"   -> Direct execution: {'SUCCESS' if direct_success else 'FAILED'} (Time: {direct_time:.4f}s)")
        
        # Calculate difference and percentage overhead
        time_diff = sandbox_time - direct_time
        if direct_time > 0:  # Avoid division by zero
            percentage = (time_diff / direct_time) * 100
        else:
            percentage = 0
        
        print(f"   -> Sandbox overhead: {time_diff:.4f}s ({percentage:.2f}%)")
        
        # Store results for visualization
        performance_results["command"].append(' '.join(cmd))
        performance_results["sandbox_time"].append(sandbox_time)
        performance_results["direct_time"].append(direct_time)
        performance_results["time_difference"].append(time_diff)
        performance_results["time_percentage"].append(percentage)
    else:
        print("   -> Direct execution: SKIPPED (unsafe command)")
        
    # Update safe/unsafe counts as before
    if sandbox_success:
        results['safe'] += 1
        print("   -> Result: SAFE ✅")
    else:
        results['unsafe'] += 1
        print("   -> Result: BLOCKED/UNSAFE ❌")
