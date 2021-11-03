import cv2
from obj_detection import *
from line_follow import linefollow
#from robo_AI import *
import time

def cam(q):
    cap = cv2.VideoCapture(0)
    cap.set(3,640.0) #set the size
    cap.set(4,480.0)  #set the size
    print("cap")
    detect = False
    line_follower = False
    colour_detect = False
    follow_obj = False
    myModel = mnSSD("ssd-mobilenet-v2", 0.5)
    data = ''
    while True:
        #data =  conn.recv()
        _, img = cap.read()
        if not q.empty():
            data = q.get()
            if data == "detect":
                detect = True
            elif data == "follow_line":
                line_follower = True
            elif data == "detect colour":
                colour_detect=True
            elif data == "follow object":
                follow_obj = True
        if detect:
            objects = myModel.detect(img,  True)
            if len(objects)!=0:
                print(objects[0][0])
                if objects[0][0]=="person":
                        #print(objects[0][0])
                    print(objects[0][0],img_reco(img, True))
        if line_follower:
            linefollow(img)
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if data == "END":
            break
        if key ==27:
            break

      

    cap.release()
    cv2.destroyAllWindows()

if __name__ =="__main__":
    cam()
        
   