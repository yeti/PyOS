from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM
from random import random, randint

PORT = 11999
HOST = ''

class ProcessCreator(Thread):

    def __init__(self, os):
        super(ProcessCreator, self).__init__()
        self.os = os
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind((HOST, PORT))
        self.daemon = True
        self.start()

    def run(self):
        while True:
            self.sock.recv(1024)
            self.os.add_job(*self.generate_random_job())

    @staticmethod
    def generate_random_job():
        steps = randint(10, 1000)
        mem = randint(1, 30)
        net_usage = ProcessCreator.random_intervals()
        usb_usage = ProcessCreator.random_intervals()
        return steps, mem, net_usage, usb_usage
                
    @staticmethod
    def random_intervals():
        num_of_intervals = randint(0, 3)
        last_end = 0
        usage = []
        for i in range(num_of_intervals):
            start = random() * 0.5 + last_end
            end = start + 0.2
            if end <= 1:
                usage.append((start, end))
                last_end = end
            else:
                break
        return usage

