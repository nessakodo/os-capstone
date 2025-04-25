# sandbox.py (COMPLETED)
# This file helps us run bad-script.sh with or without sandboxing.
# It saves the output of each run in the /logs folder so we can compare results later.

import subprocess # lets us run terminal commands
from datetime import datetime # adds the current date/time to log filenames
import os # helps us create folders and deal with file paths


# This function runs a command (like a script) and writes the output directly to a log file
def _log_and_run(command, tag):
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/{tag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    attempted = 0
    blocked = 0

    with open(log_file, "w") as f:
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            for line in process.stdout:
                f.write(line)

                if "[ACTION:" in line:
                    attempted += 1
                if "Permission denied" in line or "Operation not permitted" in line:
                    blocked += 1

            process.wait()
            print(f"[{tag.upper()}] Log saved to {log_file}")
            print(f"[{tag.upper()}] Actions attempted: {attempted}, Blocked: {blocked}")
            return attempted, blocked  # ✅ return result

        except Exception as e:
            f.write(f"Error: {str(e)}\n")
            print(f"[{tag.upper()}] Failed to run script")
            return 0, 0  # Fallback

def run_with_firejail():
    command = ["firejail", "--quiet", "./bad-script.sh"]
    return _log_and_run(command, "sandboxed")

def run_without_firejail():
    command = ["./bad-script.sh"]
    return _log_and_run(command, "unsandboxed")