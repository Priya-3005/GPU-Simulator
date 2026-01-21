from gpu import GPU

class BaselineAutoscaler:
    def __init__(self, scale_threshold=5):
        self.scale_threshold = scale_threshold

    def scale_if_needed(self, cluster):
        if len(cluster.queue) > self.scale_threshold:
            # Always add expensive GPU (H100)
            new_gpu = GPU("H100", speed=2.0, memory=141, cost=2.0)
            cluster.add_gpu(new_gpu)
            print("Autoscaler: Added H100 GPU")
