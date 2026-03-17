from simulator import Simulator
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

policies = ["static", "scale_up", "basic", "smart"]

results = {}
metrics_summary = []


# TO RUN SIMULATION FOR EACH POLICY

for policy in policies:
    print(f"\nRunning Policy: {policy.upper()}")

    sim = Simulator(sim_time=300, policy=policy)
    cluster = sim.run()

    jobs = cluster.completed_jobs
    data = []

    for job in jobs:
        latency = job.latency()
        data.append({
            "latency": latency,
            "sla": job.sla,
            "sla_violation": latency > job.sla
        })

    df = pd.DataFrame(data)


    # Realistic Cloud Cost Calculation (Active Time Based)
    total_cost = cluster.calculate_total_cost(sim.sim_time)


    df["sla_gap"] = df["latency"] - df["sla"]

    violation_rate = df["sla_violation"].mean() * 100
    avg_latency = df["latency"].mean()

    positive_gaps = df[df["sla_gap"] > 0]["sla_gap"]
    sla_severity = positive_gaps.mean() if len(positive_gaps) > 0 else 0

    cost_per_job = total_cost / len(jobs)

    results[policy] = df

    metrics_summary.append({
        "Policy": policy,
        "Total Cost": round(total_cost, 2),
        "Avg Latency": round(avg_latency, 2),
        "SLA Violation %": round(violation_rate, 2),
        "SLA Severity": round(sla_severity, 2),
        "Cost per Job": round(cost_per_job, 2)
    })



summary_df = pd.DataFrame(metrics_summary)
print("\n===== POLICY COMPARISON =====")
print(summary_df)
print("=============================\n")



# COMPARATIVE SLA GAP PLOT


plt.figure()
plt.axhline(y=0, linestyle='--')

for policy in policies:
    plt.plot(results[policy]["sla_gap"].values, label=policy)

plt.title("SLA Gap Comparison Across Policies")
plt.xlabel("Job Index")
plt.ylabel("Latency - SLA")
plt.legend()
plt.show()

# COMPARATIVE CDF OF SLA GAP

plt.figure()

for policy in policies:
    sorted_gap = np.sort(results[policy]["sla_gap"].values)
    cdf = np.arange(len(sorted_gap)) / float(len(sorted_gap))
    plt.plot(sorted_gap, cdf, label=policy)

plt.axvline(x=0, linestyle='--')
plt.title("CDF of SLA Gap Across Policies")
plt.xlabel("Latency - SLA")
plt.ylabel("Cumulative Probability")
plt.legend()
plt.show()



# SLA VIOLATION RATE BAR CHART

plt.figure()
plt.bar(summary_df["Policy"], summary_df["SLA Violation %"])
plt.title("SLA Violation Rate Comparison")
plt.xlabel("Policy")
plt.ylabel("Violation Percentage")
plt.show()



# COST COMPARISON BAR CHART

plt.figure()
plt.bar(summary_df["Policy"], summary_df["Total Cost"])
plt.title("Total Cost Comparison")
plt.xlabel("Policy")
plt.ylabel("Total Cost")
plt.show()
