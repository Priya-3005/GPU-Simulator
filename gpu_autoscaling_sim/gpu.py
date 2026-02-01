class GPU:
    def __init__(self, gpu_type, speed, memory, cost):
        self.type = gpu_type
        self.speed = speed
        self.memory = memory
        self.cost = cost
        self.busy = False
        self.current_job = None
        self.remaining_time = 0
        self.total_busy_time = 0

        # To scale down GPUs when not in use
        self.idle_time = 0

    def assign_job(self, job, current_time):
        self.busy = True
        self.current_job = job
        job.start_time = current_time
        self.remaining_time = job.compute / self.speed

    # def update(self, time_step=1):
    #     if self.busy:
    #         self.remaining_time -= time_step
    #         self.total_busy_time += time_step
    #         if self.remaining_time <= 0:
    #             self.busy = False
    #             self.current_job.end_time = self.current_job.start_time + (self.current_job.compute / self.speed)
    #             self.current_job = None 
    
    def update(self, time_step=1):
        completed_job = None

        if self.busy:
            self.remaining_time -= time_step
            self.total_busy_time += time_step
            self.idle_time = 0

            if self.remaining_time <= 0:
                completed_job = self.current_job
                self.busy = False
                completed_job.end_time = completed_job.start_time + (completed_job.compute / self.speed)
                self.current_job = None 
                
        else: 
            self.idle_time += time_step

        return completed_job

