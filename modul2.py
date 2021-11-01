#!/usr/bin/python3
import jetson.inference
import jetson.utils
import cv2
from main_video3 import *
class mnSSD():
    def __init__(self, path, threshold):
        self.path = path
        self.threshold = threshold
        self.net = jetson.inference.detectNet(self.path, self.threshold)
    
    def detect(self, img, display = False):
        imgCuda = jetson.utils.cudaFromNumpy(img)
        detections = self.net.Detect(imgCuda, overlay = "OVERLAY_NONE")
        objects = []
        print(f'FPS: {int(self.net.GetNetworkFPS())}')
        for d in detections:
            className = self.net.GetClassDesc(d.ClassID)
            objects.append([className,d])
            
            if display:
                cx, cy = int(d.Center[0]),int(d.Center[1])
                x1,y1,x2,y2 = int(d.Left),int(d.Top),int(d.Right),int(d.Bottom)
                cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),2)
                cv2.circle(img, (cx,cy),5,(0,255,0),cv2.FILLED)
                cv2.line(img,(x1,cy),(x2,cy),(0,255,0),1)
                cv2.line(img,(cx,y1),(cx,y2),(0,255,0),1)
                cv2.putText(img, className, (x1+5,y1+5),cv2.FONT_HERSHEY_DUPLEX,0.75,(255,0,255),2)
                cv2.putText(img, f'FPS: {int(self.net.GetNetworkFPS())}', (30,30),cv2.FONT_HERSHEY_DUPLEX,1,(255,0,0),2)
        return objects


def main():
    

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    myModel = mnSSD("ssd-mobilenet-v2", 0.5)
    while True:
        #name = input("ENTER...")
        _, img = cap.read()
        _, img2= cap.read()

        img_reco(img)
        objects = myModel.detect(img, True)
        if len(objects)!=0:
            if objects=="person":
                print(objects[0][0])
                img_reco(img)
        detect(img, img2)
 
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
