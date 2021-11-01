import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
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
while True:
    dis = DistanceSensor()
    print(dis.getDistance())
    #time.sleep(1)