# action_comparison.py
import matplotlib.pyplot as plt
import os
from collections import defaultdict

def parse_log_file(log_file):
    """Parse log file and count blocked/allowed actions by type"""
    action_stats = defaultdict(lambda: {'attempted': 0, 'blocked': 0})
    current_action = None
    
    with open(log_file) as f:
        for line in f:
            if line.startswith('[ACTION:'):
                action_type = line.split(':')[1].strip().strip(']')
                current_action = action_type
                action_stats[current_action]['attempted'] += 1
            elif 'Permission denied' in line or 'cannot touch' in line:
                if current_action:
                    action_stats[current_action]['blocked'] += 1
    
    return action_stats

def generate_comparison_chart(sandboxed_log, unsandboxed_log, output_path):
    """Generate grouped bar chart comparing action results"""
    sandboxed_stats = parse_log_file(sandboxed_log)
    unsandboxed_stats = parse_log_file(unsandboxed_log)
    
    # Get all unique action types
    action_types = sorted(set(sandboxed_stats.keys()).union(set(unsandboxed_stats.keys())))
    
    # Prepare data for plotting
    sandboxed_allowed = []
    sandboxed_blocked = []
    unsandboxed_allowed = []
    unsandboxed_blocked = []
    
    for action in action_types:
        sandboxed_allowed.append(sandboxed_stats[action]['attempted'] - sandboxed_stats[action]['blocked'])
        sandboxed_blocked.append(sandboxed_stats[action]['blocked'])
        unsandboxed_allowed.append(unsandboxed_stats[action]['attempted'] - unsandboxed_stats[action]['blocked'])
        unsandboxed_blocked.append(unsandboxed_stats[action]['blocked'])
    
    # Plot configuration
    bar_width = 0.35
    index = range(len(action_types))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create bars
    bar1 = ax.bar(index, unsandboxed_allowed, bar_width, label='Allowed (Unsandboxed)', color='lightgreen')
    bar2 = ax.bar(index, unsandboxed_blocked, bar_width, bottom=unsandboxed_allowed, 
                 label='Blocked (Unsandboxed)', color='salmon')
    
    bar3 = ax.bar([i + bar_width for i in index], sandboxed_allowed, bar_width, 
                 label='Allowed (Sandboxed)', color='green')
    bar4 = ax.bar([i + bar_width for i in index], sandboxed_blocked, bar_width, 
                 bottom=sandboxed_allowed, label='Blocked (Sandboxed)', color='red')
    
    # Customize plot
    ax.set_xlabel('Action Type')
    ax.set_ylabel('Number of Actions')
    ax.set_title('Sandboxing Effectiveness by Action Type')
    ax.set_xticks([i + bar_width/2 for i in index])
    ax.set_xticklabels(action_types)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Visualization saved to {output_path}")

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("visuals", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Find most recent log files
    log_files = sorted([f for f in os.listdir('logs') if f.endswith('.log')], reverse=True)
    
    if len(log_files) >= 2:
        sandboxed_log = os.path.join('logs', log_files[0])  # Most recent is sandboxed
        unsandboxed_log = os.path.join('logs', log_files[1])
        
        print(f"Comparing:\n- Sandboxed: {sandboxed_log}\n- Unsandboxed: {unsandboxed_log}")
        generate_comparison_chart(sandboxed_log, unsandboxed_log, "visuals/action_type_comparison.png")
    else:
        print("Error: Need at least 2 log files for comparison")
        print("Run sandbox_simulation.py first to generate logs")