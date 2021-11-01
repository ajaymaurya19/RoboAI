import cv2
import numpy as np
from robo_AI import setServoAngle


setServoAngle(0)
setServoAngle(90)
cap = cv2.VideoCapture(0)

'''cap.set(3, 480)
cap.set(4, 320)'''

_, frame = cap.read()

resize = cv2.resize(frame, (480, 320)) 
rows, cols, _ = resize.shape
print(resize.shape)
x_medium = int(cols / 2)
center = int(cols / 2)
position = 90 # degrees
while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (480, 320))
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # red color
    lower_blue = np.array([90,60,0])
    upper_blue = np.array([121,255,255])
    '''lower_green = np.array([40,70,80])
    upper_green = np.array([70,255,255])'''
    '''low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])'''
    red_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y),(x+w, y+h),(0,255,0),2)
        
        x_medium = int((x + x + w) / 2)
        break
    
    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
    
    cv2.imshow("Frme", frame)
    cv2.imshow("Frame", red_mask)
    
    
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
    # Move servo motor
    if x_medium < center -40:
        position += 5
        setServoAngle(position) 
    elif x_medium > center + 40:
        position -= 5
        setServoAngle(position) 
     
    #pwm.setServoPosition(0, position)
    
cap.release()
cv2.destroyAllWindows()
