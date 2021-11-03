from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
pan = 32
tilt = 33
GPIO.setup(tilt, GPIO.OUT) # white => TILT
GPIO.setup(pan, GPIO.OUT) # gray ==> PAN
def setServoAngle(servo, angle):
	assert angle >=45 and angle <= 150
	pwm = GPIO.PWM(servo, 50)
	pwm.start(0)
	dutyCycle = angle / 18. + 3.
	pwm.ChangeDutyCycle(dutyCycle)
	sleep(0.3)
	pwm.stop()

def angle(an1, an2):
    setServoAngle(pan, an1)
    # 70 t0 150
    setServoAngle(tilt, an2)
if __name__ == '__main__':  
    for i in range (60, 150, 10):
        angle(i, i)
        #50 to 100
        
    
    for i in range (150, 60, -10):
        angle(i, i)
    
        
    setServoAngle(pan, 100)
    setServoAngle(tilt, 70)    
    GPIO.cleanup()