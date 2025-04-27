# test.py
# CLI-based sandbox testing script for OS Capstone Project
# Some structure and visualization concepts inspired with help from ChatGPT suggestions,
# refined and customized by team to fit our project requirements.

import subprocess
import sys
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
def visualize_results(results):
    """Creates a simple bar chart showing safe vs unsafe commands."""
    labels = ['Safe', 'Unsafe']
    values = [results['safe'], results['unsafe']]

    plt.bar(labels, values, color=['green', 'red'])
    plt.title('Sandboxed Command Safety Results')
    plt.ylabel('Number of Commands')
    plt.tight_layout()
    plt.savefig('visuals/test_summary.png')
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[!] No command provided.") # updated to print when no command
        print("Usage: python3 test.py <command> [arguments]") # shows how the script should be used
        print("Running example attack commands and generating visual instead...\n") # temporary placeholder
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
            else:
                results['unsafe'] += 1

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

