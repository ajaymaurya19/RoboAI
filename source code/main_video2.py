import cv2
from simple_facerec import SimpleFacerec
from datetime import datetime

now = datetime.now()
dtString = now.strftime('%d/%b/%Y, %H:%M:%S')

def makeAttendanceEntry(name):
    with open('/media/nvidi/nvidia/robo_AI/source code/listt.csv','r+') as f:
        allLines = f.readlines()
        attendanceList = []
        for line in allLines:
            entry = line.split(',')
            attendanceList.append(entry[0])
        if name not in attendanceList:
            now = datetime.now()
            dtString = now.strftime('%d/%b/%Y, %H:%M:%S')
            f.writelines(f'\n{name},{dtString}')


def img_reco(img):
    face_locations, face_names = sfr.detect_known_faces(img)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        makeAttendanceEntry(name)
        cv2.putText(img, name,(x1, y1 - 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(img, (x1-4, y1-54), (x2+4, y2+4), (0, 0, 200), 4)

def detect(img):
    img2 = img.copy()
    diff = cv2.absdiff(img, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print(f"Object detected")


# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("/media/nvidi/nvidia/robo_AI/source code/images/")

# Load Camera
cap = cv2.VideoCapture(0)

count = 0
face_id = 7
while True:
    _, img = cap.read()

    '''ret, img = cap.read()
    ret, img2 = cap.read()'''

    # Detect Faces
    '''face_locations, face_names = sfr.detect_known_faces(img)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        makeAttendanceEntry(name)
        cv2.putText(img, name,(x1, y1 - 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(img, (x1-4, y1-54), (x2+4, y2+4), (0, 0, 200), 4)'''

        #cv2.imwrite("/media/word/nvidia/robo_AI/source code/dataset/User." + str(face_id) + '.' + str(count) + ".jpg", frame[y1-50:y2,x1:x2])

        #count += 1
    
    '''diff = cv2.absdiff(img, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print(f"Object detected")'''


    
    cv2.imshow("Frame", img)

    key = cv2.waitKey(1)
    if key == 27:
        break
    elif count >= 100: # Take 30 face sample and stop video
        break
cap.release()
cv2.destroyAllWindows()