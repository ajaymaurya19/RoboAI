import cv2
import numpy as np
img =cv2.imread('Ajay.jpeg')
lowerThreshold = 127
edges = cv2.Canny(img,lowerThreshold,lowerThreshold*2)
contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #cv2.cv.CV_CHAIN_APPROX_NONE or cv2.cv.CV_CHAIN_APPROX_SIMPLE

#Select longest contour as this should be the capsule
lengthC=0
ID=-1
idCounter=-1
for x in contours:
    idCounter=idCounter+1 
    if len(x) > lengthC:
        lengthC=len(x)
        ID=idCounter

if ID != -1:
    cnt = contours[ID]
    cntFull=cnt.copy()

    #approximate the contour, where epsilon is the distance to 
    #the original contour
    cnt = cv2.approxPolyDP(cnt, epsilon=1, closed=True)

    #add the first point as the last point, to ensure it is closed
    lenCnt=len(cnt)
    cnt= np.append(cnt, [[cnt[0][0][0], cnt[0][0][1]]]) 
    cnt=np.reshape(cnt, (lenCnt+1,1, 2))

    lenCntFull=len(cntFull)
    cntFull= np.append(cntFull, [[cntFull[0][0][0], cntFull[0][0][1]]]) 
    cntFull=np.reshape(cntFull, (lenCntFull+1,1, 2))

    #find the moments
    M = cv2.moments(cnt)
    MFull = cv2.moments(cntFull)
    print('Area = %.2f \t Area of full contour= %.2f' %(M['m00'], MFull['m00']))