from pickle import NONE
import cv2
from simple_facerec import SimpleFacerec
from datetime import datetime


now = datetime.now()
dtString = now.strftime('%d/%b/%Y, %H:%M:%S')
sfr = SimpleFacerec()
#sfr.load_encoding_images("/media/nvidi/nvidia/robo_AI/source code/images/")
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

def img_reco(img, display = False):
    face_locations, face_names = sfr.detect_known_faces(img)
    for face_loc, name in zip(face_locations, face_names):
      
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        makeAttendanceEntry(name)
        if display:
            cv2.putText(img, name,(x1, y1 - 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(img, (x1-4, y1-54), (x2+4, y2+4), (0, 0, 200), 4)

        return face_loc


def detect(img, img2):
    
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
        return True
        '''x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print(f"Object detected")'''

if __name__=="__main__":
    # Encode faces from a folder
    sfr = SimpleFacerec()
    #sfr.load_encoding_images("/media/nvidi/nvidia/robo_AI/source code/images/")

    # Load Camera
    cap = cv2.VideoCapture(0)

    '''count = 0
    face_id = 7
    while True:
        _, img = cap.read()
        _, img2 = cap.read()
        #img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

            #cv2.imwrite("/media/word/nvidia/robo_AI/source code/dataset/User." + str(face_id) + '.' + str(count) + ".jpg", frame[y1-50:y2,x1:x2])
            #count += 1
        img_reco(img)
        #detect(img, img2)
        cv2.imshow("Frame", img)
        key = cv2.waitKey(1)
        if key == 27:
            break
        elif count >= 100: # Take 30 face sample and stop video
            break'''
    while 1:
        ret, img = cap.read()
        #img = cv2.flip(img, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces =img_reco(img)
        print(faces)
        #y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        if faces is not NONE:
            for (y,w,h,x) in faces:
                #servoPosition(int(x+w/2), int(y+h/2))
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                '''roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]'''
                #servoPosition(int(x+w/2), int(y+h/2))
                print (int(x+w/2), int(y+h/2))
            '''yes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)'''
        cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()