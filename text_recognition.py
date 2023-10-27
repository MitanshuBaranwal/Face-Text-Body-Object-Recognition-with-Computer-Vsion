# for changing tesseract location based on os
import platform

import cv2
###### TEXT RECOGNITION ######
import pytesseract
###### for adding time ######
from time import strftime
############ for creating events folder ##########
import os
###### Added for creating consolidated dataframe ######
import pandas as pd

text_count = 0
text_ts_df = pd.DataFrame()


def text_recognition(image_path, user_id):
    global text_count
    global text_ts_df
    text_ts = []
    text_ts_final = []
    text_recognized_final = ""
    if platform.system() == 'Windows':
        pytesseract.pytesseract.tesseract_cmd = os.path.join("dependencies", "text_recognition", "Tesseract-OCR",
                                                             "tesseract.exe")
    else:
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

    frame = cv2.imread(image_path)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    text_recognized = pytesseract.image_to_string(img)
    if text_recognized:
        text_count = text_count + 1
        cv2.putText(frame, text_recognized, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    if text_count > 0:
        return 1
    else:
        return 0

#user_id  = 100
#image_path = r"C:\Users\Downloads\TechSmith-Blog-ExtractText.png"
#print(text_recognition(image_path,user_id))
