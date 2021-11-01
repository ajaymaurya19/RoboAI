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




# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("/media/nvidi/nvidia/robo_AI/source code/images/")

# Load Camera
cap = cv2.VideoCapture(0)

count = 0
face_id = 7
while True:
    ret, frame = cap.read()

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        makeAttendanceEntry(name)
        cv2.putText(frame, name,(x1, y1 - 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1-4, y1-54), (x2+4, y2+4), (0, 0, 200), 4)



        #cv2.imwrite("/media/word/nvidia/robo_AI/source code/dataset/User." + str(face_id) + '.' + str(count) + ".jpg", frame[y1-50:y2,x1:x2])

        count += 1
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
    elif count >= 100: # Take 30 face sample and stop video
        break
cap.release()
cv2.destroyAllWindows()