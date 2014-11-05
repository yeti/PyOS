from PyOS import PyOS
from time import sleep 

os = PyOS(10, 100)
os.add_job(500, 14, [(0.5, 0.75)], [(0.25, 0.75)])
os.add_job(500, 35, [(0.5, 0.75)], [(0.25, 0.75)])
os.add_job(500, 10, [(0.5, 0.75)], [(0.25, 0.75)])

while True:
    sleep(5)
    for job in os.jobs:
        if not job.done.is_set():
            break
    else:
        print("\n\n\nall jobs are done!\n\n\n")
