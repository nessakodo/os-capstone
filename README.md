# OS Capstone – Securing the System: Sandboxing as a Modern OS Security Mechanism

A Python-based simulation and visualization project exploring how sandboxing mechanisms in modern operating systems prevent unauthorized access to system resources.

---

## Project Overview

**Goal:**  
Simulate and visualize the difference between sandboxed and non-sandboxed processes, analyze attack scenarios, and evaluate the effectiveness of sandboxing strategies in Linux, Windows, and Docker.

---

## Team Members
- Vanessa Benavente  
- Killian Bertsch  
- Mohammad Besharat  
- Matthew Ruediger  

---

## Key Features

- Simulates actions of sandboxed vs. non-sandboxed processes  
- Charts showing blocked vs. allowed actions  
- System diagrams for Linux, Windows, Docker sandboxing  
- Security metrics for file, network, and privilege scenarios  
- Research summaries and architectural comparisons

---

## Setup & Dependencies

```bash
pip install matplotlib networkx
```
Running the Simulation
``` python 
sandbox_simulation.py
```
Outputs will be saved to the /results/ folder for use in the final report and presentation.

## File/Folder Overview

sandbox_simulation.py – Main runner file

process.py – Process class for behavior and permissions

sandbox.py – Sandbox logic and system logging

attack_scenarios.py – Attack scenario definitions

visualize.py – Chart generation (Matplotlib & NetworkX)

research/ – Summaries of Linux, Windows, and Docker sandboxing

results/ – Chart outputs (PNG, PDF)

report/ – Final PDF template and slides

---

## Deliverables

⬜️ Full Python Source Code (in this repo)

⬜️ Matplotlib-based Visualization Outputs

⬜️ Project Report and References (PDF in /report)[]

⬜️ Presentation Slides (PowerPoint)[]

