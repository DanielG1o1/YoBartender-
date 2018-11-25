# This imports the necessary libraries that the program utilizes
import cv2
import numpy as np
import sqlite3
import os

# Object used to form connection to the already existing database
conn = sqlite3.connect('database2.db')

# Object is bounded to the database connection and used to execute cammands that utilizes the database
c = conn.cursor()

# Object calls the training file that was created trainer_Ver1.1_AJ
fname = "recognizer/trainingData.yml"

# This exits the program if training file does not exists
if not os.path.isfile(fname):
    print("Please train the data first")
    exit(0)

# 'CascadeClassifier' allows specification for the cascade to be used, and will  be read from a file which, in this case, is 'haarcascadeFrontalfaceDefault_Ver1.0.xml'
face_cascade = cv2.CascadeClassifier('haarcascadefrontalfacedefault_Ver1.0.xml')

# Object captures live video footage from a camera connected to the computer
cap = cv2.VideoCapture(0)

# Object initializes face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# This trains the face recognizer with the training file
recognizer.read(fname)

# This loops the following code until an teminating condition is found
while True:
    ret, img = cap.read() # Object captures each frame of the live video footage
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Object stores the greyscale version of each frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)# Object detects faces in gray frames

    # This loops for each face found in a gray frame
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)# This creates a box around the face 
        ids,conf = recognizer.predict(gray[y:y+h,x:x+w])# Object determines if the face is similar to a face in the training file(isd) and by how much(conf) 
        c.execute("SELECT Drink_Preference FROM users WHERE id = (?);", (ids,))# This calls data from database linked to the face in the training file
        result = c.fetchall() # Object stores the data called from the database
        drink = result[0][0] # Object stores the users drink preference 
        if conf < 50:# conf< 50 is an accurate prediction
            cv2.putText(img, drink, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)# This inputs the users drink preference on the bottom edge of the box
        else:
            cv2.putText(img, 'No Match', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)# This inputs the "No Match" on the bottom edge of the box

    cv2.imshow('Face Recognizer',img)# This creates a window that shows the live feed with facial recognition implemented
    k = cv2.waitKey(30) & 0xff # Object value is inputted from the keyboard
    if k == 27:# This continues to the next line if "Esc" is pressed on the keyboard 
        break# This ends the loop

# This stops the live feed from the camera
cap.release()

# This destroys all windows created
cv2.destroyAllWindows()