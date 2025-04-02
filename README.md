## 🐍 **CPU Scheduling Visualizer**

A **Python-based simulation and visualization tool** for various CPU scheduling algorithms, developed for the Operating Systems Capstone Project (Spring 2025).

---

### 💡 **Project Overview**

This project simulates classic CPU scheduling algorithms and visually represents their execution using Gantt charts. Users can input process data (via CSV or command line), run simulations, and compare key scheduling metrics. The final deliverables will include code, documentation, and a presentation.

---

### 🧰 **Technologies Used**
- **Python** – Core logic and simulations  
- **matplotlib** – Gantt chart and metric visualization  
- **pandas** *(optional)* – Data handling for process input/output  

---

### 👥 **Team Members**
- **Vanessa Benavente**  
- **Killian Bertsch**  
- **Mohammad Besharat** 
- **Matthew Ruediger** 

---

### 📂 **Project Structure**
```
cpu_scheduling_visualizer/
├── algorithms/
│   ├── fcfs.py
│   ├── sjf.py
│   ├── priority.py
│   ├── round_robin.py
├── utils/
│   ├── gantt_chart.py
│   ├── metrics.py
├── data/
│   └── sample_processes.csv
├── main.py
├── README.md
```

---

### 📈 **Metrics Calculated**
- **Average Waiting Time**
- **Average Turnaround Time**
- **CPU Utilization**

Each algorithm will be evaluated based on these core metrics, allowing for comparative performance analysis.

---

### 📊 **Visualization**
We use **Gantt charts** to display the order and timing of process execution. Summary tables of performance metrics will accompany each visualization.

---

### 📅 **Timeline**
Refer to our project plan here:  
📄 [Google Doc – Project Plan & Roadmap](https://docs.google.com/document/d/1eA5NiAm82pLu_9Wijjbpgge6M829EuBv035WaOfV5nY/edit?usp=sharing)

---

### ✅ **How to Run the Project** *(to be completed)*
Instructions for running the simulation from the command line or GUI will be provided once development is complete.


---

### ⚙️ Tech Stack  
- **Language:** Python  
- **Libraries:**  
  - `matplotlib` – For Gantt chart generation  
  - `pandas` – For input/output processing (optional)  
- **Input Format:** CSV file or command line input  
- **Output Format:** Visual charts and printed metrics
