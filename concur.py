import threading
from time import time, sleep

def sleep_and_print(seconds):
    sleep(seconds)
    print("I'm done sleeping!")

start_time = time()
for seconds in range(10):
    threading.Thread(target=sleep_and_print, args=[seconds]).start()

while threading.active_count() > 1:
    pass
end_time = time()
print("The operation took %3f seconds" % (end_time - start_time))
