from threading import Thread, Lock, Event 
from ScalarResource import CPUResource, MemoryResource
from BoolResource import NetworkResource, USBResource
from ProcessCreator import ProcessCreator
from Job import Job

class PyOS:
    pid = 0
    pid_mutex = Lock()
    job_mutex = Lock()

    def __init__(self, total_cpu, total_mem):
        self.cpu = CPUResource(total_cpu)
        self.mem = MemoryResource(total_mem)
        self.network = NetworkResource()
        self.usb = USBResource()
        self.resources = {NetworkResource.name: self.network, USBResource.name: self.usb}
        self.process_creator = ProcessCreator(self)
        self.jobs = []

    def lock_cpu_and_memory(self):
        res1, res2 = self.cpu, self.mem
        both_locked = False
        while not both_locked:
            res1.mutex.acquire()
            both_locked = res2.mutex.acquire(False)
            if both_locked:
                return
            print("Failed to acquire %s" % res2.name)
            res1.mutex.release()
            res1, res2 = res2, res1

    def release_cpu_and_memory(self):
        self.cpu.mutex.release()
        self.mem.mutex.release()

    def acquire_cpu_and_memory(function, *args, **kwargs):
        def locked(self, *args, **kwargs):
            self.lock_cpu_and_memory()
            result = function(self, *args, **kwargs)
            self.release_cpu_and_memory()
            return result
        return locked

    @acquire_cpu_and_memory
    def add_job(self, cpu_steps, mem_per_step, net_sched, usb_sched):
        with PyOS.pid_mutex:
            PyOS.pid += 1
            job = Job(PyOS.pid, cpu_steps, mem_per_step, net_sched, usb_sched, self)
            self.cpu.add_job()
            self.mem.add_job()
            self.jobs.append(job)
            job.start()
    
    @acquire_cpu_and_memory
    def run_process(self, process):
        steps_taken = self.calc_number_of_steps(process) 
        print("Process %d took %3f steps; %3f left" % (process.pid, steps_taken, process.cpu_steps - process.total_steps - steps_taken))
        return steps_taken

    def calc_number_of_steps(self, process):
        available_cpu = self.cpu.per_job
        available_mem = self.mem.per_job
        print("Available CPU and Mem for PID %d are %3f and %3f" % (process.pid, available_cpu, available_mem))
        if available_mem < process.mem_per_step:
            return available_cpu * (available_mem / float(process.mem_per_step))
        else:
            return available_cpu

    def acquire(self, process, resources):
        for res in self.resources:
            resource = self.resources[res]
            resource.get(process)
            process.locked_resources.append(resource)
        return True

    @acquire_cpu_and_memory
    def kill(self, process):
        with self.job_mutex:
            self.jobs.remove(process)
            self.cpu.remove_job()
            self.mem.remove_job()
            print("removed pid %d" % process.pid)

#    def acquire(self, process, resources):
#        if len(resources) == 1:
#            resource = self.resources[resources[0]]
#            resource.get(process)
#            process.locked_resources.append(resource)
#            print("%s acquired %s" % (process.pid, resource))
#            return True
#        else:
#            print("Process %s requires %s" % (process.pid, resources))
#            for res in resources:
#                resource = self.resources[res]
#                if resource in process.locked_resources:
#                    continue
#                elif resource.get(process, False):
#                    print("Process %s acquired %s easily" % (process.pid, res))
#                    process.locked_resources.append(resource)
#                else:
#                    if resource.get_user().blocked:
#                        print("%s is going to steal %s from %s" % (process.pid, resource.name, resource.get_user()))
#                        resource.get_user().release_all_resources.set()
#                        resource.get(process, True)
#                        print("%s got %s" % (process.pid, resource.name))
#                        process.locked_resources.append(resource)
#                    else:
#                        print("Process %s is blocked because of %s, which is owned by %s who is finished %s" % (process.pid, res, resource.get_user().pid, resource.get_user().done.is_set()))
#                        print("Process %s blocks %s, and process %s blocks %s" % (process.pid, process.locked_resources, resource.get_user().pid, resource.get_user().locked_resources))
#                        process.blocked = True
#                        break
#            else:
#                return True
#            return False
#
    def get_process_for_release(self, process1, process2):
       return process1 if process1.pid < process2.pid else process2


