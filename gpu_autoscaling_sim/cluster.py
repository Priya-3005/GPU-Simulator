from gpu import GPU

class Cluster:
    def __init__(self):
        self.gpus = []
        self.queue = []
        self.completed_jobs = []
        self.removed_gpus = []

    def add_gpu(self, gpu):
        self.gpus.append(gpu)
    
    def remove_idle_gpu(self, idle_threshold=20):

        if len(self.gpus) <= 1:
            return  # Always keep at least one GPU

        for gpu in self.gpus:
            if not gpu.busy and gpu.idle_time >= idle_threshold:
                print(f"Autoscaler: Removing idle {gpu.type} GPU")
                self.gpus.remove(gpu)
                break  # remove only one per timestep 
    
    def average_utilization(self, current_time):
        if current_time == 0:
            return 0

        total_util = 0

        for gpu in self.gpus:
            util = gpu.total_busy_time / current_time   # Calculates utilization of each GPU
            total_util += util

        return total_util / len(self.gpus) if self.gpus else 0      #Returns cluster average utilization



    def add_job(self, job):
        self.queue.append(job)

    def schedule(self, current_time):
        for gpu in self.gpus:
            if not gpu.busy and self.queue:
                job = self.queue.pop(0)
                if job.memory <= gpu.memory:
                    gpu.assign_job(job, current_time)
                else:
                    self.queue.insert(0, job)

    # def update_gpus(self, time_step=1):
    #     for gpu in self.gpus:
    #         was_busy = gpu.busy
    #         gpu.update(time_step)
    #         if was_busy and not gpu.busy:
    #             self.completed_jobs.append(gpu.current_job) 

    def update_gpus(self, time_step=1):
        for gpu in self.gpus:
            completed_job = gpu.update(time_step)
            if completed_job:
                self.completed_jobs.append(completed_job)
