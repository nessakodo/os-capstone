# test.py
# CLI-based sandbox testing script for OS Capstone Project
# Some structure and visualization concepts inspired with help from ChatGPT suggestions,
# refined and customized by team to fit our project requirements.

import subprocess
import sys
import os
import matplotlib.pyplot as plt # added for plotting

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

