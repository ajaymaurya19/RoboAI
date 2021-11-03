from time import time
from robo_move3 import angle
from robo_move3 import Motor

rightMotor = Motor(13, 16)
leftMotor = Motor(22, 24)
for i in range (60, 150, 10):
    angle(i, i)
        #50 to 100
leftMotor.goBackward() 
rightMotor.goForward() 
time.sleep(5)
leftMotor.goForward() 
rightMotor.goBackward()
for i in range (150, 60, -10):
    angle(i, i)
    