from gpu import GPU

class AutoScaler:
    def __init__(self, cluster, sla):
        self.cluster = cluster
        self.sla = sla

        # Available GPU types (your novelty!)
        self.gpu_types = [
            {"type": "L40S", "speed": 1.0, "memory": 48, "cost": 0.5},
            {"type": "A100", "speed": 1.5, "memory": 80, "cost": 1.0},
            {"type": "H100", "speed": 2.0, "memory": 141, "cost": 2.0},
        ]

    def scale_if_needed(self, job_queue):
        if len(job_queue) > 5:
            job = job_queue[0]  # look at next job
            best_gpu = self.select_best_gpu(job)

            if best_gpu:
                gpu = GPU(
                    best_gpu["type"],
                    speed=best_gpu["speed"],
                    memory=best_gpu["memory"],
                    cost=best_gpu["cost"]
                )
                self.cluster.add_gpu(gpu)
                print(f"Autoscaler: Added {best_gpu['type']} GPU")
            else:
                print("Autoscaler: No GPU type can meet SLA")

    def select_best_gpu(self, job):
        candidates = []

        for gpu in self.gpu_types:
            est_latency = job.compute / gpu["speed"]

            if est_latency <= self.sla:
                candidates.append((gpu, est_latency))

        if not candidates:
            return None

        # Choose cheapest GPU that meets SLA
        candidates.sort(key=lambda x: x[0]["cost"])
        return candidates[0][0]
