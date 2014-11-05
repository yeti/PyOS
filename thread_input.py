import threading
from time import sleep 

def non_blocking_input():
    while True:
        s = raw_input("Type a message!")
        print s

counter = 0
t = threading.Thread(target=non_blocking_input)
t.daemon = True
t.start()

while True:
    print "The counter is %d" % counter
    counter += 1
    sleep(1)
