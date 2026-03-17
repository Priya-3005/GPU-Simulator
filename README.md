Hybrid SLA-Aware GPU Autoscaler

A simulation-based framework for intelligent GPU resource management in cloud environments, designed to optimize **SLA compliance, latency, and cost** using a hybrid autoscaling strategy.

---

## 📌 Ideology

With the growing demand for GPU-intensive workloads such as deep learning inference, efficient resource allocation in cloud environments has become critical. Traditional autoscaling approaches either:

- Focus only on performance (high cost), or  
- Focus only on cost (poor SLA compliance)

This project proposes a **Hybrid SLA-Aware GPU Autoscaler** that dynamically balances:

- ⚡ Performance (Latency)
- 📉 SLA Violations
- 💰 Cost (Realistic Cloud Pricing)

---

## 🎯 Key Features

- ✅ **Heterogeneous GPU Support** (L40S, A100, H100)
- ✅ **Job-Specific SLA Handling**
- ✅ **Dynamic Workload Simulation**
- ✅ **Four Policy Comparison Framework**
- ✅ **Realistic Cloud Cost Model (Active-Time Billing)**
- ✅ **Advanced Metrics:**
  - SLA Gap Analysis
  - SLA Severity
  - CDF Distribution
  - Cost per Job

---

## ⚙️ Autoscaling Policies Implemented

| Policy     | Description |
|------------|------------|
| **Static** | Fixed GPU, no scaling |
| **Scale-Up** | Adds GPUs based on load, no removal |
| **Basic** | Simple scale-up + scale-down |
| **Smart (Proposed)** | Hybrid SLA-aware + cost-aware scaling |

---

## 🧠 Proposed Smart Policy

The **Smart Hybrid Autoscaler** introduces:

- 📊 SLA-aware scaling decisions  
- 📈 Utilization-based scaling  
- ⏳ Idle-time threshold for GPU removal  
- 🔁 Cooldown mechanism to prevent oscillation  
- 💸 Cost-aware removal (removes most expensive GPU first)  

---

## 💰 Cost Model

Unlike traditional simulations, this project uses: 
# Cost = GPU Hourly rate * Active Time, 
where active time is the time between the creation and removal of GPU instance. 
---

## 📊 Evaluation Metrics

- Average Latency  
- SLA Violation Rate (%)  
- SLA Severity  
- Total Cost  
- Cost per Job  
- SLA Gap Distribution  
- CDF of SLA Gap  

---

## 📊 Visualizations

The project includes:

- 📉 SLA Gap Comparison
- 📈 CDF of SLA Gap
- 📊 SLA Violation Bar Chart
- 📊 Cost Comparison
- 📉 Latency vs SLA Plot

---

