from cluster import Cluster
# from autoscaler import BaselineAutoscaler
from autoscaler import AutoScaler

from job import Job
import random 
from gpu import GPU


class Simulator:
    def __init__(self, sim_time=300):
        self.sim_time = sim_time
        #self.sla = 120
        self.cluster = Cluster()
        self.autoscaler = AutoScaler(self.cluster)
        self.time = 0
        self.jobs = []
        # self.job_queue = []

    def generate_jobs(self):
        for t in range(self.sim_time):
            if random.random() < 0.3:
                compute = random.randint(50, 150)
                memory = random.randint(10, 40)
                sla = random.randint(80, 150)
                job = Job(t, compute, memory, sla)
                self.jobs.append(job)

    def run(self):
        self.generate_jobs()

        self.cluster.add_gpu(GPU("H100", speed=2.0, memory=141, cost=2.0))

        for t in range(self.sim_time):
            self.time = t

            
            for job in self.jobs:
                if job.arrival_time == t:
                    self.cluster.add_job(job)

            self.cluster.schedule(t)

            #self.autoscaler.scale_if_needed(self.cluster.queue) 
            self.autoscaler.scale_if_needed(t)


            self.cluster.update_gpus()

        return self.cluster
