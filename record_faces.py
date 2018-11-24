import cv2
import numpy as np 
import sqlite3
import os

conn = sqlite3.connect('database2.db')

if not os.path.exists('./dataset'):
    os.makedirs('./dataset')

four_dig_id = 1000
NEXT_USER = "Y"

#This LARGE loop will ensure that persons can be entered one after the other
while (NEXT_USER == 'Y'):
  four_dig_id = four_dig_id + 1
  c = conn.cursor()
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  cap = cv2.VideoCapture(0)
  uname = input("Enter your name: ")
  udrink = input("Enter your drink preference: ")
  #ushot = input("Enter your shot preference('NULL' if none): ")


  #This inserts all the data that the users entered, into the database
  c.execute('INSERT INTO users (Name, Drink_Preference, Four_Digit_Identifier) VALUES (?,?,?)', (uname,udrink,four_dig_id))
  uid = c.lastrowid
  
  #End data insertion
  #This will snap the faces
  sampleNum = 0
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
  #End snapping faces
  #Checks to see if another user must be entered

  print("Enter new user? (Press 'Y' for YES & 'N' for NO")
  NEXT_USER = input("---->")
  #End check to continue
  
#End all data capture


cap.release()
conn.commit()
conn.close()
cv2.destroyAllWindows()