class Job:
    def __init__(self, arrival_time, compute, memory, sla):
        self.arrival_time = arrival_time
        self.compute = compute
        self.memory = memory
        self.sla = sla
        self.start_time = None
        self.end_time = None

    def latency(self):
        if self.end_time is None:
            return None
        return self.end_time - self.arrival_time
