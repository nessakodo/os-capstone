# vibey ! 
# action_comparison.py
import matplotlib.pyplot as plt
from sandbox import run_with_firejail, run_without_firejail
import os

def main():
    print("=== Starting Sandbox Comparison Test ===")
    
    # Ensure visuals directory exists
    os.makedirs("visuals", exist_ok=True)
    print("Created 'visuals' directory for output")

    # Run tests with progress indicators
    print("\nRunning unsandboxed test...")
    unsandboxed_attempted, unsandboxed_blocked = run_without_firejail()
    
    print("\nRunning sandboxed test...")
    sandboxed_attempted, sandboxed_blocked = run_with_firejail()

    # Calculate metrics
    unsandboxed_allowed = unsandboxed_attempted - unsandboxed_blocked
    sandboxed_allowed = sandboxed_attempted - sandboxed_blocked
    
    # Print detailed results
    print("\n=== Test Results ===")
    print(f"Unsandboxed: {unsandboxed_allowed} allowed, {unsandboxed_blocked} blocked")
    print(f"Sandboxed: {sandboxed_allowed} allowed, {sandboxed_blocked} blocked")
    
    effectiveness = (sandboxed_blocked / sandboxed_attempted * 100) if sandboxed_attempted > 0 else 0
    print(f"\nSandbox Effectiveness: {effectiveness:.1f}% of actions blocked")

    # Visualization
    print("\nGenerating visualization...")
    labels = ['Unsandboxed', 'Sandboxed']
    allowed = [unsandboxed_allowed, sandboxed_allowed]
    blocked = [unsandboxed_blocked, sandboxed_blocked]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(labels, allowed, label='Allowed', color='green')
    ax.bar(labels, blocked, bottom=allowed, label='Blocked', color='red')

    ax.set_ylabel('Number of Actions')
    ax.set_title('Sandboxing Effectiveness')
    ax.legend()

    output_path = "visuals/action_comparison.png"
    plt.savefig(output_path)
    print(f"Visualization saved to {output_path}")

    # Show the plot (optional - may not work in all environments)
    try:
        plt.show()
    except:
        print("Note: Plot display not available in this environment")

if __name__ == "__main__":
    main()