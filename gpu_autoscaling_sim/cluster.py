from gpu import GPU

class Cluster:
    def __init__(self):
        self.gpus = []
        self.queue = []
        self.completed_jobs = []

    def add_gpu(self, gpu):
        self.gpus.append(gpu)

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
