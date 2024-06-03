#from google.cloud import storage
#from firebase_admin import credentials, db
import jetson.inference
import jetson.utils
import cv2
import numpy as np
import time 
import main
import json

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

#camera = jetson.utils.videoSource("/dev/video0")      # '/dev/video0' for V4L2
#display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

vidCap = cv2.VideoCapture("/dev/video0")
vidCap.set(3, 640)
vidCap.set(4, 480)
isDetected = False

while(True):
    ret, frame = vidCap.read()
    if ret==False: 
        print("[x] ERROR: no video frames read")
        break
    # Display the result
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    cudaImg = jetson.utils.cudaFromNumpy(frameRGB)

    detections = net.Detect(cudaImg)

    bottle = None
    #isDetected = False
    number = 0
    for detection in detections:
        bottle = (net.GetClassDesc(detection.ClassID) == 'bottle')
        if bottle and not isDetected:
                number += 1
                isDetected = False
                left, top, right, bottom = int(detection.Left), int(detection.Top), 			int(detection.Right), int(detection.Bottom)
                cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
                cv2.imwrite("test.png", frame)
                print('bottle here')
                #sending the data
                main.addImage("test.png")
                #time.sleep(2)
        else: 
               isDetected = True
               if isDetected:
                   print('bottle not here')
                   main.add_stock("bottle")

               if bottle:
                   isDetected = False
    cv2.imshow('OUTPUT', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

vidCap.release()
cv2.destroyAllWindows()
