
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO

cap = cv2.VideoCapture(0)
cap.set(3,640.0) #set the size
cap.set(4,480.0)
sensitivity = 15
lower_white = np.array([0,0,168])
upper_white = np.array([255,255,255])

while True:	
	_,image = cap.read()
	Blackline = cv2.inRange(image, lower_white, upper_white)	
	kernel = np.ones((3,3), np.uint8)
	Blackline = cv2.erode(Blackline, kernel, iterations=5)
	Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
	contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	if len(contours_blk) > 0:	 
	 blackbox = cv2.minAreaRect(contours_blk[0])
	 (x_min, y_min), (w_min, h_min), ang = blackbox
	 if ang < -45 :
	  ang = 90 + ang
	 if w_min < h_min and ang > 0:	  
	  ang = (90-ang)*-1
	 if w_min > h_min and ang < 0:
	  ang = 90 + ang	  
	 setpoint = 320
	 error = int(x_min - setpoint) 
	 ang = int(ang)	 
	 box = cv2.boxPoints(blackbox)
	 box = np.int0(box)
	 cv2.drawContours(image,[box],0,(0,0,255),3)	 
	 cv2.putText(image,str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
	 cv2.putText(image,str(error),(10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
	 cv2.line(image, (int(x_min),200 ), (int(x_min),250 ), (255,0,0),3)
	 
	  	
	cv2.imshow("orginal with line", image)	
	cv2.imshow("mask", Blackline)
	key = cv2.waitKey(1) & 0xFF	
	if key == ord("q"):
		break

GPIO.output(40, GPIO.LOW)