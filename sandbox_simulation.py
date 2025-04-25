# sandbox_simulation.py (COMPLETED)
# Calls helper functions to run a malicious script with and without sandboxing/Firejail 

import os
from sandbox import run_with_firejail, run_without_firejail

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)  # Ensure /logs exists
    run_without_firejail()
    run_with_firejail()
