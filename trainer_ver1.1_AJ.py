import os
import cv2
import numpy as np 
from PIL import Image  # Importing from the Python Image Library.

recognizer = cv2.face.LBPHFaceRecognizer_create()    # Creating the OpenCv face recognizer called the LBPH recognizer.
path = 'dataset'
if not os.path.exists('./recognizer'):
    os.makedirs('./recognizer')


def getImagesWithID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []  # Declaring faces as an empty list.
    IDs = []    # Declaring IDs as and empty list. 
    for imagePath in imagePaths:    # Looks for the path of the images.
        faceImg = Image.open(imagePath).convert('L')    # Converts image into Grayscale.
        faceNp = np.array(faceImg, 'uint8')    # Converting into a numpy array and using "unit8" as type.
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)    # Turns image into a numpy array.
        IDs.append(ID)
        cv2.imshow("training", faceNp)
        cv2.waitKey(10)
    return np.array(IDs), faces


Ids, faces = getImagesWithID(path)
recognizer.train(faces, Ids)  # Putting the training data such as faces and Ids for the recognizer to train.
recognizer.save('recognizer/trainingData.yml')
cv2.destroyAllWindows()
