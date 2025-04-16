# OS Capstone – Securing the System: Sandboxing as a Modern OS Security Mechanism

A Python-based simulation and visualization project exploring how sandboxing mechanisms in modern operating systems help prevent unauthorized access to system resources through process isolation and restricted execution environments.

---

## Project Overview

To demonstrate the behavioral differences between sandboxed and non-sandboxed processes through the use of real-world attack simulations. This project explores how sandboxing mechanisms—specifically using [Firejail](https://github.com/netblue30/firejail) on Ubuntu—enhance operating system security by isolating processes and restricting access to sensitive system resources.

---

## Team Members
- Vanessa Benavente  
- Killian Bertsch  
- Mohammad Besharat  
- Matthew Ruediger  

---

## **Project Scope**  
Each team member will implement Firejail locally to simulate how sandboxing prevents unauthorized file access, network misuse, and privilege escalation. By running pseudo-malicious scripts in both sandboxed and unrestricted environments, we collect and analyze logs to assess the effectiveness of various isolation techniques.

### This work applies core OS principles:
- **Process Isolation** – Keeps processes from interfering with one another  
- **Access Control** – Limits access to files, devices, and commands  
- **System Call Management** – Filters unsafe syscalls via kernel mechanisms like seccomp  
- **Resource Management** – Restricts CPU, memory, and I/O usage in sandboxed contexts  

We present visualizations, effectiveness scores, and architecture diagrams to compare sandboxing in Linux (Firejail), Windows (AppContainer), and **(possibly)** Docker.


---

## Setup Instructions

### Prerequisites

- Ubuntu 20.04 or greater
- Python 3.x
- Firejail

### Installation
**Clone the Repositry**

   ```bash
   git clone https://github.com/yourusername/os-capstone.git
   cd os-capstone
  ```

**Install Dependences**

   ```bash
   sudo apt update
   sudo apt install firejail docker.io python3-pip
   pip3 install -r requirements.txt
  ```

---

## Running the Simulation

**Execute the Main Scipt**

   ```bash
   python3 sandbox_simulation.py
  ```


**View Reslts**

*Outputs will be saved to the /results/ folder for use in the final report and presentation.*


## Deliverables

**Full Source Code** (in this repo)

**Matplotlib-based Visualization Outputs** (in /visuals)

**Presentation Slides:** [Capstone Powerpoint](https://olucdenver-my.sharepoint.com/:p:/g/personal/vanessa_benavente_ucdenver_edu/EdDpQnrzFnlJigiEMT-agQ8B8_FfiwXYSOkmdRw0xIx8AA?e=jwRJB0)

**Project Report:** [Research Report](https://docs.google.com/document/d/1F-AweAtG0pEalSz2Hs1eE6Vv7kvXwJZo6tNyZNBZ-HE/edit?tab=t.0)
