from pickle import NONE
import cv2
import numpy as np
import multiprocessing

def get():
        
        #cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture(0)
        while True:

                frame = video(cap)

                cv2.imshow("frame", frame)

                key = cv2.waitKey(1)
                if key == 27: #Key 'S'
                        break
        cv2.waitKey(0)
        cv2.destroyAllWindows() 

def video(cap):
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        return frame

if __name__ == "__main__":
        p1 = multiprocessing.Process(target = get)
        p1.start()
        #p1.join()
        #cap = cv2.VideoCapture(0)
        '''while True:

                frame = video(cap)

                cv2.imshow("frame", frame)

                key = cv2.waitKey(1)
                if key == 27: #Key 'S'
                        break
        cv2.waitKey(0)
        cv2.destroyAllWindows() '''