import cv2

cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("c", frame)
    cv2.imshow("img", img)
    key = cv2.waitKey(1)
    if key == 27:
        break 

cap.release()
cv2.destroyAllWindows()