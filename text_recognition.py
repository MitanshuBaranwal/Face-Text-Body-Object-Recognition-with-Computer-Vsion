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
    #current_time = strftime("%H:%M:%S %d/%m/%Y")
    if text_recognized:
        text_count = text_count + 1
        #text_ts = [current_time]
        #text_recognized_final = text_recognized_final + text_recognized

        # saving the snapshots
        # dirname = os.path.join("outputs", "events", "text_on_screen", "{}".format(user_id))
        # try:
        #     os.makedirs(dirname, exist_ok=True)
        #     #print("new folder for user created")
        # except:
        #     pass
        #folder_time = strftime("%Y%m%d%H%M%S")
        #file = os.path.join(dirname, '{}{}.jpg'.format(user_id, folder_time))
        cv2.putText(frame, text_recognized, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        #cv2.imwrite(file, frame)

        # append to pandas dataframe
        #text_ts.append(text_recognized)
        #the below commented line was commented because frame.append will be removed in future
        #text_ts_df = text_ts_df.append(pd.Series(text_ts), ignore_index=True)
        #text_ts_df = pd.concat([text_ts_df, pd.Series(text_ts)], ignore_index=True)
    #print(text_recognized_final)
    if text_count > 0:
        return 1
    else:
        return 0

#user_id  = 100
#image_path = r"C:\Users\Downloads\TechSmith-Blog-ExtractText.png"
#print(text_recognition(image_path,user_id))