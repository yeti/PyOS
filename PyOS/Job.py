from threading import Thread, Lock, Event 
from BoolResource import NetworkResource, USBResource

class Job(Thread):

    def __init__(self, pid, cpu_steps, mem_per_step, net_sched, usb_sched, os):
        super(Job, self).__init__()
        self.pid = pid
        self.cpu_steps = cpu_steps
        self.total_steps = 0
        self.mem_per_step = mem_per_step
        self.net_sched = net_sched
        self.usb_sched = usb_sched
        self.os = os
        self.locked_resources = []
        self.blocked = False
        self.release_all_resources = Event()
        self.done = Event()
        self.daemon = True

    def run(self):
        while not self.done.is_set():
            if self.release_all_resources.is_set():
                self.free_resources()
            else:
                self.take_step()
        self.os.kill(self)

    def take_step(self):
        resources = self.required_resources()
        if resources:
            print("Resources required are %s" % resources)
            if not self.os.acquire(self, resources):
                return
        self.total_steps += self.os.run_process(self)
        self.free_resources()
        if self.cpu_steps <= self.total_steps:
            self.done.set()
    
    def free_resources(self):
        for resource in self.locked_resources:
            resource.release()
        self.locked_resources = []
        self.blocked = False
        self.release_all_resources.clear()

    def required_resources(self):
        resources = []
        schedules = [(self.net_sched, NetworkResource.name), (self.usb_sched, USBResource.name)]
        for schedule, resource in schedules:
            if schedule:
                ratio = float(self.total_steps) / float(self.cpu_steps)
                for start, end in schedule:
                    if ratio >= start and ratio <= end:
                        resources.append(resource)
                        break
        return resources

