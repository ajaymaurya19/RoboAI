import multiprocessing as mp
import time

def fun_1():
    while True:
        time.sleep(2)
        print("hi")

def fun_2():
    while True:
        time.sleep(2)

        
        print("Enter")


 

if __name__ == "__main__":
    p1 = mp.Process(target=fun_1)
    p2 = mp.Process(target=fun_2)
    p1.start()
    p2.start()

 
