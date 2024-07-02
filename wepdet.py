import cv2
import numpy as np
from saveimage import imgwrite
from mailcode import send_emails, send_mails, email_to_list, email_to_list1
from message import mes
import time

def WD(v,mail=[]):#pass v value to function to detect
    start_time = time.time()
    email_to_list1.append(mail)
    net = cv2.dnn.readNet("pretrainedweightfile.weights", "configfile.cfg")#reading our model
    classes = ["Weapon"]

    output_layer_names = net.getUnconnectedOutLayersNames()
    colors = np.random.uniform(0, 255, size=(len(classes), 3))#RGB
    cap = cv2.VideoCapture(v)#if v==0 then video capture
    while True:
        _, img = cap.read()
        if not _:
            print("Error: Failed to read a frame from the video source.")
            break
        height, width, channels = img.shape

    # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layer_names)

    # Showing information on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        print(indexes)
        if indexes == 0:
            print("weapon detected in frame")

        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
                try:
                    mes()
                    fname=imgwrite(img)
                    if email_to_list1 == ['']:
                        send_emails(email_to_list,fname)#sent to default mail
                    else:
                        #print("s",email_to_list1,"e")
                        send_mails(email_to_list1,fname)#sending mail to registered user mail
                except Exception as e:
                    print(e,type(e))


    #frame = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        cv2.imshow("Image", img)
    #imgwrite(img)
        key = cv2.waitKey(100)#100ms
    #print(key)
        if key % 256 == 27:#if ESC is pressed code will be exited
            break
        current_time = time.time()
    #print(current_time)
        elapsed_time = current_time - start_time
        if elapsed_time>=60:
            break
    cap.release()
    cv2.destroyAllWindows()

#for detecting images and videos
def WD1(v1,mail=[]):#pass v value to function to detect
    start_time = time.time()
    email_to_list1.append(mail)
    net = cv2.dnn.readNet("pretrainedweightfile.weights", "configfile.cfg")
    classes = ["Weapon"]

    output_layer_names = net.getUnconnectedOutLayersNames()
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    cap = cv2.VideoCapture(v1)
    while True:
        _, img = cap.read()
        if not _:
            print("Error: Failed to read a frame from the video source.")
            break
        height, width, channels = img.shape
    

    # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        #using 1/255 or 0.00392  we are converting int to float (416,416) resizes the image True refers to swapRB

        net.setInput(blob)
        outs = net.forward(output_layer_names)

    # Showing information on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        print(indexes)
        if indexes == 0:
            print("weapon detected in frame")

        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
                try:
                    mes()
                    fname=imgwrite(img)
                    if email_to_list1 == ['']:
                        send_emails(email_to_list,fname)
                    else:
                        send_mails(email_to_list1,fname)
                except Exception as e:
                    print(e,type(e))


    #frame = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        cv2.imshow("Image", img)
    #imgwrite(img)
        key = cv2.waitKey(100)
    #print(key)
        if key % 256 == 27:           #Press ESC to stop live detection
            break
        current_time = time.time()
    #print(current_time)
        elapsed_time = current_time - start_time
        if elapsed_time>=60:
            break
    cap.release()
    cv2.destroyAllWindows()