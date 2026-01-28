from simulator import Simulator
import pandas as pd
import matplotlib.pyplot as plt

sim = Simulator(sim_time=300)
cluster = sim.run()

jobs = cluster.completed_jobs
data = []

for job in jobs:
    data.append({
        "arrival": job.arrival_time,
        "latency": job.latency(),
        "sla": job.sla,
        "sla_violation": job.latency() > job.sla
    })

df = pd.DataFrame(data)

total_cost = 0
for gpu in cluster.gpus:
    total_cost += gpu.cost * 300

print("Total GPUs:", len(cluster.gpus))
print("Total Cost:", total_cost)
print("Average Latency:", df["latency"].mean())
print("SLA Violations:", df["sla_violation"].mean() * 100, "%")

plt.figure()
plt.plot(df["latency"], label="Latency")
plt.axhline(y=df["sla"].mean(), color='r', linestyle='--', label="Avg SLA")
plt.legend()
plt.title("Job Latency")
plt.show()
