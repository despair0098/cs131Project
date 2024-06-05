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
#botFlag = False
#appFlag = False
#banFlag = False
#app_printed = False
#app_not_printed = False
i = 0
j = 0
k = 0

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
    numBot = 0
    numApp = 0
    numBan = 0
    
    if i == 0:
        botFlag = 2
        appFlag = 2
        banFlag = 2

    for detection in detections:
        bottle = (net.GetClassDesc(detection.ClassID) == 'bottle')
        if bottle:
                numBot += 1
                left, top, right, bottom = int(detection.Left), int(detection.Top), 			int(detection.Right), int(detection.Bottom)
                cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
                cv2.imwrite("bottle.png", frame)
                #if botFlag == 0:
                #    break;
                botFlag = 1
                #sending the data
                main.addImage("bottle.png")
                #time.sleep(2)
        else: 
                botFlag = 3

    for detection in detections:
        apple = (net.GetClassDesc(detection.ClassID) == 'apple')
        if apple:
                numApp += 1
                left, top, right, bottom = int(detection.Left), int(detection.Top), 			int(detection.Right), int(detection.Bottom)
                cv2.rectangle(frame, (left, top), (right, bottom), (255,255,0), 2)
                cv2.imwrite("apple.png", frame)
                #if appFlag == 0:
                #    break;
                appFlag = 1
                """
                if not app_printed:
                   print("apple here")
                   app_printed = True
                break;
                """
                #sending the data
                main.addImage("apple.png")
                #time.sleep(2)
        else: 
                appFlag = 3
    """
    if not appFlag:
       if not app_not_printed:
          print("apple not here")
          apple_not_printed = True
    """
          
    for detection in detections:
        banana = (net.GetClassDesc(detection.ClassID) == 'banana')
        if banana:
                numBan += 1
                left, top, right, bottom = int(detection.Left), int(detection.Top), 			int(detection.Right), int(detection.Bottom)
                cv2.rectangle(frame, (left, top), (right, bottom), (0,255,255), 2)
                cv2.imwrite("banana.png", frame)
                if banFlag == 0:
                    break;
                banFlag = 1
                #sending the data
                main.addImage("banana.png")
                #time.sleep(2)
        else: 
                banFlag = 3

    if botFlag == 1:
        i += 1
        #print("i is", i)
        if(i == 5):
           print("bottle here")
        botFlag = 0

    if botFlag == 3:
        if(i > 20):
           print("bottle not here")
           i = 0
        botFlag = 0
    
    if appFlag == 1:
        j += 1
        #print("i is", i)
        if(j == 5):
           print("apple here")
        appFlag = 0

    if appFlag == 3:
        if(j > 20):
           print("apple not here")
           j = 0
        appFlag = 0
    
    if banFlag == 1:
        k += 1
        #print("i is", i)
        if(k == 5):
           print("banana here")
        banFlag = 0

    if banFlag == 3:
        if(k > 20):
           print("banana not here")
           k = 0
        banFlag = 0

    cv2.imshow('OUTPUT', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

vidCap.release()
cv2.destroyAllWindows()
