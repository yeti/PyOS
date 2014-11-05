import socket
from ProcessCreator import HOST, PORT

def add_jobs():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT + 1))
    while True:
        num_of_jobs = input("How many jobs would you like to start?")
        for i in range(num_of_jobs):
            sock.sendto("Start", (HOST, PORT))

add_jobs()
