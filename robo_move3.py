from datetime import date
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)
GPIO.setup(33, GPIO.OUT)
# This class is used to control a DC motor.
class Motor:
    def __init__(self, IN1, IN2):
        
        self.forward = IN1
        self.backward = IN2
    

        # pins setup
 
        GPIO.setup(self.forward, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.backward, GPIO.OUT, initial=GPIO.LOW)
       

    def goForward(self):
        GPIO.output(self.forward, GPIO.HIGH)
        GPIO.output(self.backward, GPIO.LOW)

    def goBackward(self):
        GPIO.output(self.forward, GPIO.LOW)
        GPIO.output(self.backward, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.forward, GPIO.LOW)
        GPIO.output(self.backward, GPIO.LOW)


    

    def __del__(self):
        # cleanup and leave pins in the safe state
        self.stop()
     
        GPIO.cleanup([self.forward, self.backward])

class DistanceSensor:
    def __init__(self, TRIGGER = 11, ECHO=12):
        self.trig = TRIGGER
        self.echo = ECHO

    # This function returns distance in cm or -1 value if the measurement failed.
    # Distance measurement using a ultrasonic sensor is a time-sensitive work.
    # So, because here runs Ubuntu OS, I think it depends by process scheduling.
    # Sometimes it work with an error of max 2 cm, sometimes it doesn't.
    # Doesn't work for distance < 4 cm (echo pulse is too fast ~230us).
    def getDistance(self):
        # pins setup
        GPIO.setup(self.trig, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.echo, GPIO.IN)

        # set Trigger to HIGH for 10 us
        GPIO.output(self.trig, GPIO.HIGH)
        time.sleep(0.00001) # 10 us
        GPIO.output(self.trig, GPIO.LOW)

        # start counting time at Echo rising edge
        GPIO.wait_for_edge(self.echo, GPIO.RISING, timeout=100) # 100 ms
        startTime = time.time()

        # stop counting time at Echo falling edge
        GPIO.wait_for_edge(self.echo, GPIO.FALLING, timeout=100) # 100 ms
        elapsedTime = time.time() - startTime   # in seconds

        distance = -1
        # check if the measurement succeeded
        if elapsedTime < 0.1:
            # get the distance in cm using sonic speed (aprox. 34300 cm/s)
            distance = (elapsedTime * 34300) / 2

        GPIO.cleanup([self.trig, self.echo])
    
        return distance

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
	time.sleep(0.3)
	pwm.stop()

def angle(an1, an2):
    setServoAngle(pan, an1)
    # 70 t0 150
    setServoAngle(tilt, an2)


def main_roboAI():
    
    setServoAngle(90)
    rightMotor = Motor(13, 16)
    leftMotor = Motor(22, 24)
    #rightMotor = Motor(32, 13, 16)
    
   
    angle = 90
    dis = DistanceSensor()
    move= True
    while move:
        
    
        data = dis.getDistance()
        #print(data)
    
        if data == -1:
            continue
        if data < 20:
            print('stop')
            leftMotor.stop()
            rightMotor.stop()
        if data >20:
            #print(data)
            print("goForward")
            leftMotor.goForward()
            rightMotor.goForward()
        elif data < 20: 
            print("stop")
            setServoAngle(0)
            time.sleep(1)
            left_dis = dis.getDistance()
            setServoAngle(90)

            setServoAngle(180)
            time.sleep(1)
            right_dis = dis.getDistance()
            setServoAngle(90)

            if left_dis and right_dis< 10:
                print("gobackword")
                leftMotor.goBackward()
                rightMotor.goBackward()
                time.sleep(2)
            elif left_dis > right_dis:
                print("goleft")
                leftMotor.stop()
                rightMotor.goForward()
                time.sleep(2)
            elif left_dis < right_dis:
                print('goright')
                leftMotor.goForward()
                rightMotor.stop()
                time.sleep(2)  
                


  
if __name__ == "__main__":
    #move_ret(1)
    main_roboAI()

