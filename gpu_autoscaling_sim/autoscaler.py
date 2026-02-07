from gpu import GPU

class AutoScaler:
    def __init__(self, cluster):
        self.cluster = cluster
        #self.sla = sla

        self.gpu_types = [
            {"type": "L40S", "speed": 1.0, "memory": 48, "cost": 0.5},
            {"type": "A100", "speed": 1.5, "memory": 80, "cost": 1.0},
            {"type": "H100", "speed": 2.0, "memory": 141, "cost": 2.0},
        ]

    # def scale_if_needed(self, job_queue):
    #     if len(job_queue) > 5:
    #         job = job_queue[0]  
    #         best_gpu = self.select_best_gpu(job)

    #         if best_gpu:
    #             gpu = GPU(
    #                 best_gpu["type"],
    #                 speed=best_gpu["speed"],
    #                 memory=best_gpu["memory"],
    #                 cost=best_gpu["cost"]
    #             )
    #             self.cluster.add_gpu(gpu)
    #             print(f"Autoscaler: Added {best_gpu['type']} GPU")
    #         else:
    #             print("Autoscaler: No GPU type can meet SLA")
    #     self.cluster.remove_idle_gpu() 



    def scale_if_needed(self, current_time):
        avg_util = self.cluster.average_utilization(current_time)
        queue_length = len(self.cluster.queue)

        # SCALE UP
        # if avg_util > 0.75 and queue_length > 0:
        #     job = self.cluster.queue[0]
        #     best_gpu = self.select_best_gpu(job)

        #     if best_gpu:
        #         gpu = GPU(
        #             best_gpu["type"],
        #             speed=best_gpu["speed"],
        #             memory=best_gpu["memory"],
        #             cost=best_gpu["cost"]
        #         )
        #         self.cluster.add_gpu(gpu)
        #         print(f"Autoscaler: Scaling UP - Added {best_gpu['type']} GPU")


        # SCALE UP CONDITIONS
        if queue_length > 0:

            job = self.cluster.queue[0]

            # Estimate latency using fastest GPU
            fastest_speed = max(g["speed"] for g in self.gpu_types)
            estimated_latency = job.compute / fastest_speed

            if (
                avg_util > 0.70
                or queue_length > 5
                or estimated_latency > job.sla
            ):
                best_gpu = self.select_best_gpu(job)

                if best_gpu:
                    gpu = GPU(
                        best_gpu["type"],
                        speed=best_gpu["speed"],
                        memory=best_gpu["memory"],
                        cost=best_gpu["cost"]
                    )
                    self.cluster.add_gpu(gpu)
                    print(f"Autoscaler: Scaling UP - Added {best_gpu['type']} GPU")

        # SCALE DOWN
        if avg_util < 0.30:
            for gpu in self.cluster.gpus:
                if not gpu.busy and len(self.cluster.gpus) > 1:
                    self.cluster.gpus.remove(gpu)
                    print(f"Autoscaler: Scaling DOWN - Removed idle {gpu.type} GPU")
                    break


    def select_best_gpu(self, job):
        candidates = []

        for gpu in self.gpu_types:
            est_latency = job.compute / gpu["speed"]

            if est_latency <= job.sla:
                candidates.append((gpu, est_latency))

        if not candidates:
            return None

        # Choosing cheapest GPU that meets SLA
        candidates.sort(key=lambda x: x[0]["cost"])
        return candidates[0][0]
