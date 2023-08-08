###### for Cv options
import cv2
#for adding face_recognition
import face_recognition as fr
import numpy as np


###### for adding time ######
from time import strftime
############ for creating events folder ##########
import os
###### Added for creating consolidated dataframe ######
import pandas as pd

def face_identification(image_path, user_id):
    #print(user_id)

    # Open the image file as an image using Pillow
    try:
        validation_image = fr.load_image_file(image_path)
    except:
        print("validation_image picture doesnt exist in folder")
        return("validation_image picture doesnt exist in folder")
    try:
        if __name__ == "__main__":
            file_path = r"C:\Users\Desktop\bitbucket\unlimit2\unlimiteye\outputs\captures\face\{}.jpg".format(user_id)
            #print(file_path)
            original_image = fr.load_image_file(file_path)
        else:
            file_name = "{}.jpg".format(user_id)
            file_path = os.path.join('outputs', 'captures', 'face', file_name)
            original_image = fr.load_image_file(file_path)

    except:
        print("original picture doesnt exist in folder")
        return("original picture doesnt exist in folder")
    try:
        face_encoding1 = fr.face_encodings(validation_image)[0]
    except:
        print("no face found in validation_image")
        return("no face found in validation_image")
    try:
        face_encoding2 = fr.face_encodings(original_image)[0]
    except:
        print("no face found in original_image")
        return("no face found in original_image")
    try:
        distance = fr.face_distance([face_encoding1], face_encoding2)[0]
        print(distance)
        if distance < 0.6:
            # Return a JSON response
            #print("match")
            return 0
        elif distance > 0.6:
            #print("not match")
            return 1
    except:
        print("error with original and to be validated image look above log for more info")
        return("error with original and to be validated image look above log for more info")

if __name__ == "__main__":
    user_id  = 100
    image_path = r"C:\Users\Desktop\bitbucket\unlimit2\unlimiteye\outputs\image_proctor\100_125\89587.jpg"
    print(face_identification(image_path,user_id))