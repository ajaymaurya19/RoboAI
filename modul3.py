import jetson.inference
import jetson.utils
import cv2
from main_video3 import *
#tracker = cv2.legacy.TrackerMOSSE_create()
net = jetson.inference.detectNet("ssd-mobilenet-v2", 0.5)
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
success, frame = cap.read()
imgCuda = jetson.utils.cudaFromNumpy(frame)
detections = net.Detect(imgCuda, overlay = "OVERLAY_NONE")
objects = []

for d in detections:
    className = net.GetClassDesc(d.ClassID)
    objects.append([className,d])
    display = True  
    if display:
        cx, cy = int(d.Center[0]),int(d.Center[1])
        bbox = int(d.Left),int(d.Top),int(d.Right),int(d.Bottom)
     

tracker.init(frame, bbox)


def drawBox(img,bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 3 )
    cv2.putText(img, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)



while True:
    _, img = cap.read()
 
    #success, bbox = tracker.update(img)

    if success:
        drawBox(img,bbox)
    else:
        cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.rectangle(img,(15,15),(200,90),(255,0,255),2)
    cv2.putText(img, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2);
    cv2.putText(img, "Status:", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2);



    cv2.imshow("Tracking", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
       break

cap.release()
cv2.destroyAllWindows()
