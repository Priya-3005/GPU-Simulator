# from simulator import Simulator
# import pandas as pd
# import matplotlib.pyplot as plt

# sim = Simulator(sim_time=300)
# cluster = sim.run()

# jobs = cluster.completed_jobs
# data = []

# for job in jobs:
#     data.append({
#         "arrival": job.arrival_time,
#         "latency": job.latency(),
#         "sla": job.sla,
#         "sla_violation": job.latency() > job.sla
#     })

# df = pd.DataFrame(data)

# # total_cost = 0
# # for gpu in cluster.gpus:
# #     total_cost += gpu.cost * 300

# #new addi
# total_cost = 0

# # Active GPUs
# for gpu in cluster.gpus:
#     total_cost += gpu.cost * gpu.total_busy_time

# # Removed GPUs
# for gpu in cluster.removed_gpus:
#     total_cost += gpu.cost * gpu.total_busy_time

# print("Total GPUs:", len(cluster.gpus))
# print("Total Cost:", total_cost)
# print("Average Latency:", df["latency"].mean())
# print("SLA Violations:", df["sla_violation"].mean() * 100, "%")

# # plt.figure()
# # plt.plot(df["latency"].values, label="Latency")
# # plt.axhline(y=df["sla"].mean(), color='r', linestyle='--', label="SLA threshold")
# # plt.legend()
# # plt.title("Job Latency")
# # plt.show()

# plt.figure()
# plt.plot(df["latency"].values, label="Latency")
# plt.plot(df["sla"].values, linestyle='--', label="Job SLA")
# plt.legend()
# plt.title("Job Latency vs Job-Specific SLA")
# plt.xlabel("Job Index")
# plt.ylabel("Time")
# plt.show()




#NEW main.py 

# from simulator import Simulator
# import pandas as pd
# import matplotlib.pyplot as plt

# policies = ["static", "scale_up", "basic", "smart"]

# results = {}

# def run_experiment(policy_name):
#     print(f"\nRunning Policy: {policy_name.upper()}")

#     sim = Simulator(sim_time=300, policy=policy_name)   # <-- pass policy
#     cluster = sim.run()

#     jobs = cluster.completed_jobs
#     data = []

#     for job in jobs:
#         data.append({
#             "arrival": job.arrival_time,
#             "latency": job.latency(),
#             "sla": job.sla,
#             "sla_violation": job.latency() > job.sla
#         })

#     df = pd.DataFrame(data)

#     # Cost Calculation
#     total_cost = 0

#     for gpu in cluster.gpus:
#         total_cost += gpu.cost * gpu.total_busy_time

#     for gpu in cluster.removed_gpus:
#         total_cost += gpu.cost * gpu.total_busy_time

#     metrics = {
#         "Total GPUs": len(cluster.gpus),
#         "Total Cost": total_cost,
#         "Average Latency": df["latency"].mean(),
#         "SLA Violations (%)": df["sla_violation"].mean() * 100
#     }

#     return metrics, df


# # -----------------------------
# # Run All Policies
# # -----------------------------
# for policy in policies:
#     metrics, df = run_experiment(policy)
#     results[policy] = metrics


# # -----------------------------
# # Print Comparison Table
# # -----------------------------
# print("\n\n===== POLICY COMPARISON =====")
# comparison_df = pd.DataFrame(results).T
# print(comparison_df)


# # # Cost Plot
# # fig1 = plt.figure()
# # plt.bar(comparison_df.index, comparison_df["Total Cost"])
# # plt.title("Total Cost Comparison")
# # plt.xlabel("Policy")
# # plt.ylabel("Cost")
# # plt.show()

# # # SLA Plot
# # fig2 = plt.figure()
# # plt.bar(comparison_df.index, comparison_df["SLA Violations (%)"])
# # plt.title("SLA Violation Comparison")
# # plt.xlabel("Policy")
# # plt.ylabel("Violation %")
# #plt.show()

# plt.figure(figsize=(10,5))

# plt.subplot(1,2,1)
# plt.bar(comparison_df.index, comparison_df["Total Cost"])
# plt.title("Cost")

# plt.subplot(1,2,2)
# plt.bar(comparison_df.index, comparison_df["SLA Violations (%)"])
# plt.title("SLA Violations")

# plt.tight_layout()
# plt.show()


# NEW MAIN.Py - 3 graphs

# from simulator import Simulator
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# # -----------------------------
# # RUN SIMULATION
# # -----------------------------
# sim = Simulator(sim_time=300)
# cluster = sim.run()

# jobs = cluster.completed_jobs
# data = []

# for job in jobs:
#     latency = job.latency()
#     data.append({
#         "arrival": job.arrival_time,
#         "latency": latency,
#         "sla": job.sla,
#         "sla_violation": latency > job.sla
#     })

# df = pd.DataFrame(data)

# # -----------------------------
# # COST CALCULATION (Accurate)
# # -----------------------------
# total_cost = 0

# # Active GPUs
# for gpu in cluster.gpus:
#     total_cost += gpu.cost * gpu.total_busy_time

# # Removed GPUs
# for gpu in cluster.removed_gpus:
#     total_cost += gpu.cost * gpu.total_busy_time


# # -----------------------------
# # METRICS
# # -----------------------------
# df["sla_gap"] = df["latency"] - df["sla"]

# violation_rate = df["sla_violation"].mean() * 100
# avg_latency = df["latency"].mean()

# # SLA Severity (only positive gaps)
# positive_gaps = df[df["sla_gap"] > 0]["sla_gap"]
# sla_severity = positive_gaps.mean() if len(positive_gaps) > 0 else 0

# print("\n===== EXPERIMENT RESULTS =====")
# print("Total GPUs (Active):", len(cluster.gpus))
# print("Total Cost:", round(total_cost, 2))
# print("Average Latency:", round(avg_latency, 2))
# print("SLA Violation Rate:", round(violation_rate, 2), "%")
# print("Average SLA Severity:", round(sla_severity, 2))
# print("==============================\n")


# # ==========================================================
# # 1️⃣ LATENCY VS JOB-SPECIFIC SLA
# # ==========================================================
# plt.figure()
# plt.plot(df["latency"].values, label="Latency")
# plt.plot(df["sla"].values, linestyle='--', label="Job SLA")
# plt.title("Job Latency vs Job-Specific SLA")
# plt.xlabel("Job Index")
# plt.ylabel("Time")
# plt.legend()
# plt.show()


# # ==========================================================
# # 2️⃣ SLA GAP PER JOB (VERY IMPORTANT)
# # ==========================================================
# plt.figure()
# plt.axhline(y=0, linestyle='--')
# plt.plot(df["sla_gap"].values)
# plt.title("SLA Gap per Job (Latency - SLA)")
# plt.xlabel("Job Index")
# plt.ylabel("Time Difference")
# plt.show()


# # ==========================================================
# # 3️⃣ CDF OF SLA GAP (RESEARCH LEVEL)
# # ==========================================================
# sorted_gap = np.sort(df["sla_gap"].values)
# cdf = np.arange(len(sorted_gap)) / float(len(sorted_gap))

# plt.figure()
# plt.plot(sorted_gap, cdf)
# plt.axvline(x=0, linestyle='--')
# plt.title("CDF of SLA Gap")
# plt.xlabel("Latency - SLA")
# plt.ylabel("Cumulative Probability")
# plt.show()


#MAIN 
from simulator import Simulator
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

policies = ["static", "scale_up", "basic", "smart"]

results = {}
metrics_summary = []

# ============================================
# RUN SIMULATION FOR EACH POLICY
# ============================================

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

    # Cost calculation
    # total_cost = 0
    # for gpu in cluster.gpus:
    #     total_cost += gpu.cost * gpu.total_busy_time
    # for gpu in cluster.removed_gpus:
    #     total_cost += gpu.cost * gpu.total_busy_time
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

# ============================================
# PRINT SUMMARY TABLE
# ============================================

summary_df = pd.DataFrame(metrics_summary)
print("\n===== POLICY COMPARISON =====")
print(summary_df)
print("=============================\n")


# ============================================
# 1️⃣ COMPARATIVE SLA GAP PLOT
# ============================================

plt.figure()
plt.axhline(y=0, linestyle='--')

for policy in policies:
    plt.plot(results[policy]["sla_gap"].values, label=policy)

plt.title("SLA Gap Comparison Across Policies")
plt.xlabel("Job Index")
plt.ylabel("Latency - SLA")
plt.legend()
plt.show()


# ============================================
# 2️⃣ COMPARATIVE CDF OF SLA GAP
# ============================================

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


# ============================================
# 3️⃣ SLA VIOLATION RATE BAR CHART
# ============================================

plt.figure()
plt.bar(summary_df["Policy"], summary_df["SLA Violation %"])
plt.title("SLA Violation Rate Comparison")
plt.xlabel("Policy")
plt.ylabel("Violation Percentage")
plt.show()


# ============================================
# 4️⃣ COST COMPARISON BAR CHART
# ============================================

plt.figure()
plt.bar(summary_df["Policy"], summary_df["Total Cost"])
plt.title("Total Cost Comparison")
plt.xlabel("Policy")
plt.ylabel("Total Cost")
plt.show()
