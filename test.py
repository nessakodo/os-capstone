#sandbox for testing commands given through CLI *VIBE CODED AS FUCKKKKKKK*


import subprocess
import sys

def check_command_safety(command):
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_command_safety.py <command> [arguments]")
        sys.exit(1)

    command = sys.argv[1:]
    if check_command_safety(command):
        print("-> Executing command inside firejail...")
        subprocess.run(["firejail", "--noprofile", *command])
    else:
        print("-> Command execution blocked.")
