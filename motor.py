import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

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



leftMotor = Motor(32, 22, 24)
rightMotor = Motor(32, 21, 19)


speed = 25
leftMotor.setSpeed(speed)
rightMotor.setSpeed(speed)
rightMotor.goBackward()
leftMotor.goBackward()
time.sleep(10)
leftMotor.stop()
rightMotor.goForward()
time.sleep(10)

leftMotor.stop()
rightMotor.stop()
                






