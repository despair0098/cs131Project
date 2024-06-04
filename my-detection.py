#from google.cloud import storage
#from firebase_admin import credentials, db
import jetson.inference
import jetson.utils
import cv2
import numpy as np
import time 
#import main
#import json

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

#camera = jetson.utils.videoSource("/dev/video0")      # '/dev/video0' for V4L2
#display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

vidCap = cv2.VideoCapture("/dev/video0")
vidCap.set(3, 640)
vidCap.set(4, 480)
isDetected = False
i = 0

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
    apple = None
    banana = None
    #isDetected = False
    numBot = 0
    numApp = 0
    numBan = 0
    
    if i == 0:
        botFlag = 2
        appFlag = 2
        banFlag = 2

    for detection in detections:
        bottle = (net.GetClassDesc(detection.ClassID) == 'bottle')
        #if not isDetected: 
        if bottle:
                numBot += 1
                isDetected = False
                left, top, right, bottom = int(detection.Left), int(detection.Top), 			int(detection.Right), int(detection.Bottom)
                cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
                cv2.imwrite("test.png", frame)
                if botFlag == 0:
                    break;
                botFlag = 1
                #sending the data
                #main.addImage("test.png")
                #time.sleep(2)

    for detection in detections:
        apple = (net.GetClassDesc(detection.ClassID) == 'apple')
        #if not isDetected: 
        if apple:
                numBot += 1
                isDetected = False
                left, top, right, bottom = int(detection.Left), int(detection.Top), 			int(detection.Right), int(detection.Bottom)
                cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
                cv2.imwrite("test.png", frame)
                if appFlag == 0:
                    break;
                appFlag = 1

    for detection in detections:
        banana = (net.GetClassDesc(detection.ClassID) == 'banana')
        #if not isDetected: 
        if banana:
                numBot += 1
                isDetected = False
                left, top, right, bottom = int(detection.Left), int(detection.Top), 			int(detection.Right), int(detection.Bottom)
                cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
                cv2.imwrite("test.png", frame)
                if banFlag == 0:
                    break;
                banFlag = 1

    if botFlag == 1:
        print("bottle here")
        botFlag = 0

    if appFlag == 1:
        print("apple here")
        botFlag = 0

    if banFlag == 1:
        print("banana here")
        botFlag = 0

    i = i + 1
    cv2.imshow('OUTPUT', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

vidCap.release()
cv2.destroyAllWindows()
