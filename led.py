#from Jetson import GPIO
import RPi.GPIO as GPIO
import time

#GPIO.cleanup()
#GPIO.setwarnings(False)
led =7
GPIO.setmode(GPIO.BOARD)

GPIO.setup(led, GPIO.OUT, initial=GPIO.HIGH)
      
GPIO.output(led, GPIO.HIGH)



for i in range(7):
    GPIO.output(led, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(led,GPIO.LOW)
    time.sleep(0.1)