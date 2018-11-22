import numpy as np
import cv2
import pickle
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

labels = {"Person_Name": 1}
with open("labels.pickle", 'rb') as f:
    original_labels = pickle.load(f)
    labels = {
        v: k for k, v in original_labels.items()
    }


cap = cv2.VideoCapture(0)

while(True):
    #Capture frame by frame
    ret, frame = cap.read()

    gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
    detect = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x,y,z,h) in detect:
        #print (x,y,z,h)
        roi_gray = gray [y:y+h, x:x+z] # (ycord_start, ycord_end)
        roi_color = frame [y:y+h, x:x+z]

        id_, conf = recognizer.predict(roi_gray)
        if conf >= 45: # and conf < 85:

            print(id_)
            print(labels[id_])
            font = cv2. FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)





    img_item = "1.jpg"
    cv2.imwrite (img_item, roi_color)
    color = (255, 0, 0) #BGR 0-255
    stroke = 2
    end_cord_x = x+z
    end_cord_y = y + h
    cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
    #Display resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#Release capture when done
cap.release()
cv2.destroyAllWindows()
