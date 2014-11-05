from threading import Thread, Lock, Event 

class BoolResource:
    def __init__(self):
        self.mutex = Lock()
        self.using = None

    def get(self, process, blocking=True):
        if blocking:
            self.mutex.acquire()
            self.using = process
            return True
        else:
            if self.mutex.acquire(blocking):
                self.using = process
                return True
            else:
                return False

    def release(self):
        self.mutex.release()
        self.using = None

    def get_user(self):
        return self.using

class USBResource(BoolResource):
    name = "USB"

class NetworkResource(BoolResource):
    name = "Network"


