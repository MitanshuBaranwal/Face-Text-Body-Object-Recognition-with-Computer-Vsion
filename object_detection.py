###### for Cv options
import cv2
import numpy as np

###### for adding time ######
from time import strftime
############ for creating events folder ##########
import os
###### Added for creating consolidated dataframe ######
import pandas as pd

###### declare global variables
cell_phone_count = 0
book_count = 0
def object_detection(image_path, user_id):
    global cell_phone_count
    global book_count

    cell_phone_final = []
    book_final = []
    yolo_v3_weights_path = os.path.join("dependencies", "yolov3", "yolov3.weights")
    #print(yolo_v3_weights_path)
    yolo_v3_cfg_path = os.path.join("dependencies", "yolov3", "yolov3.cfg")
    #print(yolo_v3_cfg_path)
    # load yolo dependencies for object detection
    net = cv2.dnn.readNet(yolo_v3_weights_path, yolo_v3_cfg_path)

    classes = []
    coco_names_path = os.path.join("dependencies", "yolov3", "coco.names")
    # load coco.names text file for object names
    with open(coco_names_path, "r") as f:
        classes = f.read().splitlines()

    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(100, 3))

    frame = cv2.imread(image_path)
    frame = cv2.resize(frame, (512, 256))
    height, width, ret = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 1 / 255, (320, 320), (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.4:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)
                #print(class_ids)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
    #print(indexes)
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label + " " + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)
            #print(label)

            if label in {'cell phone', 'book'}:
                current_time = strftime("%H:%M:%S %d/%m/%Y")
                if label == "cell phone":
                    cell_phone_count = cell_phone_count + 1
                    #cell_phone = [current_time]
                    #cell_phone_final.append(cell_phone)

                    # saving the snapshots
                    #dirname = os.path.join("outputs", "events", "cell_phone", "{}".format(user_id))
                    # print(dirname)
                    # try:
                    #     os.mkdir(dirname)
                    #     #print("new folder for user created")
                    # except:
                    #     # folder already exists no folder creation needed
                    #     pass
                    #folder_time = strftime("%Y%m%d%H%M%S")
                    # print(folder_time)
                    #file = os.path.join(dirname, '{}{}.jpg'.format(user_id, folder_time))
                    # print(file)
                    #cv2.imwrite(file, frame)
                    # print("capturedimage saved")
                    #print("ceell phone detectde")
                if label == "book":
                    book_count = book_count + 1
                    #book = [current_time]
                    #book_final.append(book)

                    # saving the snapshots
                    #dirname = os.path.join("outputs", "events", "book", "{}".format(user_id))
                    # print(dirname)
                    # try:
                    #     os.mkdir(dirname)
                    #     #print("new folder for user created")
                    # except:
                    #     # folder already exists no folder creation needed
                    #     pass

                    #folder_time = strftime("%Y%m%d%H%M%S")
                    # print(folder_time)
                    #file = os.path.join(dirname, '{}{}.jpg'.format(user_id, folder_time))
                    # print(file)
                    #cv2.imwrite(file, frame)
                    # print("capturedimage saved")

        #cv2.imshow("object_detection", frame)
        #cv2.waitKey(0)

    #print("cell_phone_count: ", cell_phone_count)
    #print("book_count: ", book_count)

    if book_count > 0 and cell_phone_count > 0:
        return 1,1
    elif book_count > 0:
        return 1,0
    elif cell_phone_count > 0:
        return 0,1
    else:
        return 0,0
#user_id  = 100
#image_path = r"C:\Users\Desktop\bitbucket\outputs\image_proctor\101_102\819929.jpg"
#print(object_detection(image_path,user_id))
