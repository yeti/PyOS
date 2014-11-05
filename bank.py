import threading
from time import sleep
from random import randint

class Account:
    def __init__(self, balance):
        self.balance = balance

class Transfer(threading.Thread):
    def __init__(self, one, two):
        super(Transfer, self).__init__()
        self.one = one
        self.two = two
        self.daemon = True

    def run(self):
        while True:
            self.transfer(randint(0, 10))

    def transfer(self, amount):
        self.one.balance -= amount
        self.two.balance += amount
        assert self.one.balance + self.two.balance == total, \
                "One has %d, Two has %d, the total is %d" \
                % (self.one.balance, self.two.balance, \
                self.one.balance + self.two.balance)

alice = Account(500)
bob = Account(200)
total = 700
one = Transfer(alice, bob)
two = Transfer(bob, alice)
one.start()
two.start()
while True:
    pass
