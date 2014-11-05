from threading import Thread, Lock, Event 

class ScalarResource:
    def __init__(self, total):
        self.total = total
        self.per_job = 0
        self.num_jobs = 0
        self.mutex = Lock()

    def add_job(self):
        self.num_jobs += 1
        self.update_per_job_allowance()
        
    def remove_job(self):
        self.num_jobs -= 1
        if self.num_jobs:
            self.update_per_job_allowance()

    def update_per_job_allowance(self):
        self.per_job = float(self.total) / self.num_jobs

class CPUResource(ScalarResource):
    name = "CPU"

class MemoryResource(ScalarResource):
    name = "Memory"

