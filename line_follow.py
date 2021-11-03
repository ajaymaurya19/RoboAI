import numpy as np
import cv2
from robo_move3 import *
#setServoAngle(90)
leftMotor = Motor(22, 24)
rightMotor = Motor(13, 16)
dis = DistanceSensor()
def linefollow(frame):
    if dis.getDistance() > 20:
        frame = frame[150:480, 0:640]
        kernel = np.ones((2,2),np.uint8)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        gray= cv2.medianBlur(gray, 3)   #to remove salt and paper noise
        #to binary
        ret,thresh = cv2.threshold(gray,200,255,0)  #to detect white objects
        #to get outer boundery only     
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)
        #to strength week pixels
        thresh = cv2.dilate(thresh,kernel,iterations = 5)
        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.line(frame,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(frame,(0,cy),(1280,cy),(255,0,0),1)
            cv2.drawContours(frame, contours, -1, (0,255,0), 1)
            cv2.circle(frame, (cx,cy), 5, (255,255,255), -1)
            cv2.line(frame, (220,0), (220, 480), (255,0,0),3)
            cv2.line(frame, (420,0), (420, 480), (255,0,0),3)
            print(cx)
            if cx >= 420:
                
                print("Turn Right")
                leftMotor.goForward()
                rightMotor.stop()
            if cx < 420 and cx > 220:
                print ("On Track!")
                leftMotor.goForward()
                rightMotor.goForward()
            if cx <= 220:
                print ("Turn Left!")
                leftMotor.stop()
                rightMotor.goForward()
                
        else:
            print ("I don't see the line")
            leftMotor.stop()
            rightMotor.stop()
if __name__=="__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3,640.0) #set the size
    cap.set(4,480.0)  #set the size

    
    while(True):
    
        ret, frame = cap.read()
        if dis.getDistance() > 20:
     
            linefollow(frame)
      
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
  
    cap.release()
    cv2.destroyAllWindows()
