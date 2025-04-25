# action_comparison.py (INCOMPLETE)
# Runs both sandboxed and unsandboxed versions and charts results

import matplotlib.pyplot as plt
from sandbox import run_with_firejail, run_without_firejail

# Run both tests and get their result counts
unsandboxed_attempted, unsandboxed_blocked = run_without_firejail()
sandboxed_attempted, sandboxed_blocked = run_with_firejail()

# Assume "allowed" = attempted - blocked
unsandboxed_allowed = unsandboxed_attempted - unsandboxed_blocked
sandboxed_allowed = sandboxed_attempted - sandboxed_blocked

labels = ['Allowed', 'Blocked']
x = range(len(labels))

# Bar values for each case
unsandboxed = [unsandboxed_allowed, unsandboxed_blocked]
sandboxed = [sandboxed_allowed, sandboxed_blocked]


# TODO: Plot the bar chart here w/ matplotlib
