from time import time, sleep

def sleep_and_print(seconds):
    sleep(seconds)
    print("I'm done sleeping!")

start_time = time()
for seconds in range(10):
    sleep_and_print(seconds)

end_time = time()
print("The operation took %3f seconds" % (end_time - start_time))
