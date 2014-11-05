from threading import Thread, Lock, Event
import random
import time
 
# 5 Dining philosophers with 5 forks. Must have two forks to eat.
#
# Deadlock is avoided by never waiting for a fork while holding a fork (locked)
# Procedure is to do block while waiting to get first fork, and a nonblocking
# acquire of second fork.  If failed to get second fork, release first fork,
# swap which fork is first and which is second and retry until getting both.
 
class Philosopher(Thread):
 
    running = True
    daemon = True

 
    def __init__(self, name, forkOnLeft, forkOnRight, scheduler):
        super(Philosopher, self).__init__()
        self.name = name
        self.counter = 0
        self.forkOnLeft = forkOnLeft
        self.forkOnRight = forkOnRight
        self.scheduler = scheduler
 
    def run(self):
        while(self.running):
            #  Philosopher is thinking (but really is sleeping).
            time.sleep( random.uniform(1,3))
            print '%s is hungry.' % self.name
            self.dine()
 
    def dine(self):
        fork1, fork2 = self.forkOnLeft, self.forkOnRight
 
        while self.running:
            fork1.acquire(True)
            if not self.running: break
            print("%s has acquired %s; it has been acquired %d times" % (self.name, fork1.index, fork1.counter))
            locked = fork2.acquire(False)
            if locked:
                print("%s has also acquired %d; it has been acquired %d times" % (self.name, fork2.index, fork2.counter)) 
                break
            fork1.release()
            print '%s swaps forks' % self.name
            fork1, fork2 = fork2, fork1
        else:
            return
 
        self.dining(fork1, fork2)
 
    def dining(self, fork1, fork2):			
        self.counter += 1
        print '%s starts eating for the %d-th time'% (self.name, self.counter)
        time.sleep(random.uniform(1,3))
        print '%s finishes eating, releases fork %d and fork %d and leaves to think.' % (self.name, fork1.index, fork2.index)
        fork2.release()
        fork1.release()
        
 
class Fork:
    lock = Lock()
    counter = 0

    def __init__(self, index):
        self.lock = Lock()
        self.index = index
        self.counter = 0

    def acquire(self, *args, **kwargs):
        locked = self.lock.acquire(*args, **kwargs)
        if locked:
            self.counter += 1
            self.increase_counter()
        return locked

    @classmethod
    def increase_counter(cls):
        with cls.lock:
            cls.counter += 1
            print("Fork counter is now %d" % Fork.counter)

    def release(self):
        return self.lock.release()

class Scheduler:
    analytics_have_been_printed = False

    def __init__(self):
        self.forks = [Fork(n) for n in range(1,6)]
        self.philosopherNames = ('Aristotle','Kant','Buddha','Marx', 'Russel')

        self.philosophers= [Philosopher(self.philosopherNames[i], self.forks[i%5], self.forks[(i+1)%5], self) \
                for i in range(5)]

        random.seed(507129)
        Philosopher.running = True
        for p in self.philosophers:
            p.start()


    def analytics(self):
        if not Scheduler.analytics_have_been_printed:
            Scheduler.analytics_have_been_printed = True
            print "That's enough eating"
            for fork in self.forks:
                print "Fork %d was used %d times" % (fork.index, fork.counter)
            for philosopher in self.philosophers:
                print "%s ate a total of %d times" % (philosopher.name, philosopher.counter)
            print ("Now we're finishing.")



s = Scheduler()
try:
    while True:
        pass
except KeyboardInterrupt:
    Philosopher.running = False
    s.analytics()
