import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'Attendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(image):
    encodedlist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodedlist.append(encode)
    return encodedlist

def markAttendance(name):
    with open('Attendence.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(' - ')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtstring}')




encodedListKnown = findEncodings(images)
print("Encoding Complete")

cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

    for encodeFace ,faceLoc in zip(encodesCurFrame,faceCurFrame):
        mathces = face_recognition.compare_faces(encodedListKnown,encodeFace)
        facedis = face_recognition.face_distance(encodedListKnown,encodeFace)
        print(facedis)
        mathceIndex = np.argmin(facedis)

        if mathces[mathceIndex]:
            name = classNames[mathceIndex].upper()
            # print(name)
            y1,x2,y2,x1 = faceLoc
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)

    cv2.imshow('Webcam',img)
    key = cv2.waitKey(1)

    if key == 81 or key == 113:
       break

cap.release()

print("encoding complete")