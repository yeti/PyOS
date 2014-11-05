from threading import Thread, Lock
from time import sleep

count = 0
counter_lock = Lock()

def increment_counter():
    global count
    counter_lock.acquire(True)
    count += 1
    counter_lock.release()

def count_forever():
    while True:
        increment_counter()

one = Thread(target=count_forever)
two = Thread(target=count_forever)
one.start()
two.start()
while True:
    sleep(2)
    print(count)
