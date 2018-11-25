# Importing the necessary libraries
import cv2
import numpy as np
import sqlite3
import os

# Object used to form connection to the [already existing] database
conn = sqlite3.connect('database2.db')

# Creating a new directory [if it doesn't exist] to store images of customers
if not os.path.exists('./dataset'):
    os.makedirs('./dataset')

# This variable is the ID generator. It generates a unique 4-digit Identifier    for each person from 1000-9999
four_dig_id = 1000
# Variable checks if another user wants to enter the system. It is used by LOOP A which controls the writing of information to the database and images to the 'dataset' folder
NEXT_USER = "Y"  

# This loop (LOOP A) will ensure that persons can be entered successively
while (NEXT_USER == 'Y'):  # Terminating condition
  
  four_dig_id = four_dig_id + 1  # Incrementing the ID number for assignment                                    to another person
  c = conn.cursor()  # Inititalizing a cursor for information storage

  # 'CascadeClassifier' allows specification for the cascade to be used, and will be read from a file which, in this case, is 'haarcascadeFrontalfaceDefault_Ver1.0.xml'
  face_cascade = cv2.CascadeClassifier('haarcascadeFrontalfaceDefault_Ver1.0.xml')
  cap = cv2.VideoCapture(0)
  uname = input("Enter your name: ")  # User will enter their name
  udrink = input("Enter your drink preference: ")  # User will enter their                                                      drink preference for the                                                     night

  #This inserts all the data that the users entered, and the autmaticall generated ID number into the database
  c.execute('INSERT INTO users (Name, Drink_Preference, Four_Digit_Identifier) VALUES (?,?,?)', (uname,udrink,four_dig_id))
  uid = c.lastrowid  # Specifies that each new entry should appear at the last                    empty row in the database
  
  sampleNum = 0  # This variable controls the amount of images taken to be                    stored in the 'dataset' folder
  while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
      sampleNum = sampleNum+1
      cv2.imwrite("dataset/" + uname + "." +str(uid)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
      cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
      cv2.waitKey(100)

    cv2.imshow('img',img)
    cv2.waitKey(1);
    if sampleNum > 20:
      break

  print("Enter new user? (Press 'Y' for YES & 'N' for NO")
  NEXT_USER = input("---->")  # Terminating condition is when NEXT_USER == 'N'
  
#End all data capture


cap.release()
conn.commit()  # Commits changes to the database
conn.close()  # Closes connection to the database
cv2.destroyAllWindows()  # Closes all windows that were opened during run-time