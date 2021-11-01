from time import sleep
from threading import *
class Hello(Thread):
    def run(self):
        input("ENTER...")


class Hi(Thread):
    def run(self):
        input("Enert...")

t1 = Hello()
t2 = Hi()
t1.start()
t2.start()