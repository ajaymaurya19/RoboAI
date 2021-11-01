from datetime import date
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)
GPIO.setup(33, GPIO.OUT)
# This class is used to control a DC motor.
class Motor:
    def __init__(self, EN, IN1, IN2):
        self.speed = EN
        self.forward = IN1
        self.backward = IN2
        self.pwm = None

        # pins setup
        GPIO.setup(self.speed, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.forward, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.backward, GPIO.OUT, initial=GPIO.LOW)
        # pwm setup
        self.pwm = GPIO.PWM(self.speed, 50) # frequency of pwm signal: 50Hz
        self.pwm.start(0)

    def goForward(self):
        GPIO.output(self.forward, GPIO.HIGH)
        GPIO.output(self.backward, GPIO.LOW)

    def goBackward(self):
        GPIO.output(self.forward, GPIO.LOW)
        GPIO.output(self.backward, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.forward, GPIO.LOW)
        GPIO.output(self.backward, GPIO.LOW)

    def setSpeed(self, value):
        # value must be between 0 and 100
        # 0->min speed | 100 -> max speed
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        self.pwm.ChangeDutyCycle(value)

    def __del__(self):
        # cleanup and leave pins in the safe state
        self.stop()
        self.pwm.stop()
        GPIO.cleanup([self.speed, self.forward, self.backward])

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

  
def setServoAngle(angle):
	pwm = GPIO.PWM(33, 100)
	pwm.start(5)
	dutyCycle = angle / 10 + 2.5
	pwm.ChangeDutyCycle(dutyCycle)
	time.sleep(0.3)
	pwm.stop()
area = ''
area1 = ""
def follow():
    if area1 > area:
        print("obj com")
    if area1 < area:
        print("obj appa")


def main_roboAI():
    setServoAngle(90)
    leftMotor = Motor(32, 22, 24)
    rightMotor = Motor(32, 19, 21)
    speed = 25
    leftMotor.setSpeed(speed)
    rightMotor.setSpeed(speed)
   
    angle = 90
    dis = DistanceSensor()
    while True:
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
        if data > 80:
            print(data)
            speed += 10
            if speed > 100:
                speed = 100
            leftMotor.setSpeed(speed)
            rightMotor.setSpeed(speed)
        elif data < 50:
            print(data)
            speed -= 10
            if speed < 20:
                speed = 20
            leftMotor.setSpeed(speed)
            rightMotor.setSpeed(speed)            
        
  
if __name__ == "__main__":
    main_roboAI()

