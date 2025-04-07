# CPU Scheduler Battle: Race of the Algorithms

A Python-based visualization and simulation project for comparing classic CPU scheduling algorithms in a race-style format. Built as part of our Operating Systems Capstone Project (Spring 2025), this tool demonstrates process scheduling strategies through real-time Gantt charts, metric tracking, and performance comparison.

---

## Project Overview

**Goal:**  
Simulate and visualize how different CPU scheduling algorithms handle the same workload. Each algorithm "races" to finish processing the same set of tasks, and their performance is ranked using key OS metrics.

**Core Algorithms Implemented:**
- First-Come, First-Served (FCFS)
- Shortest Job First (SJF)
- Priority Scheduling
- Round Robin

---

## Team Members
- **Vanessa Benavente**
- **Killian Bertsch**  
- **Mohammad Besharat** 
- **Matthew Ruediger** 

---

## How It Works

1. Load a set of processes (from JSON or CSV)
2. Run each algorithm on the same workload
3. Track:
   - Average Waiting Time
   - Average Turnaround Time
   - CPU Utilization
4. Visualize:
   - Gantt Charts
   - Race-style execution timeline
   - Bar charts comparing final results
   - Algorithm ranking leaderboard

---

## Output Metrics

Each algorithm returns:
```python
{
  "execution_order": [(process_id, start_time, end_time), ...],
  "metrics": {
    "avg_waiting_time": float,
    "avg_turnaround_time": float,
    "cpu_utilization": float
  }
}
```

---

## Requirements

- Python 3.x

- matplotlib

- numpy (optional, for stats)

Install dependencies:

``` bash
pip install matplotlib numpy
```

---

## Deliverables

[  ] Full Python source code (in this repo)

[  ] Matplotlib-based visualization outputs

[  ] Project Report (PDF – in /docs)

[  ] Presentation Slides (PowerPoint – in /docs)

[  ] References to recent scheduling research

---

## References & Research

