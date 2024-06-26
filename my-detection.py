import jetson.inference
import jetson.utils
import cv2
import main
import numpy as np
import time 

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

vidCap = cv2.VideoCapture("/dev/video0")
vidCap.set(3, 640)
vidCap.set(4, 480)
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
                cv2.imwrite("bottle.jpeg", frame)
                botFlag = 1

        else: 
                botFlag = 3

    for detection in detections:
        apple = (net.GetClassDesc(detection.ClassID) == 'apple')
        if apple:
                numApp += 1
                left, top, right, bottom = int(detection.Left), int(detection.Top), 			int(detection.Right), int(detection.Bottom)
                cv2.rectangle(frame, (left, top), (right, bottom), (255,255,0), 2)
                cv2.imwrite("apple.jpeg", frame)
                appFlag = 1
        else: 
                appFlag = 3
          
    for detection in detections:
        banana = (net.GetClassDesc(detection.ClassID) == 'banana')
        if banana:
                numBan += 1
                left, top, right, bottom = int(detection.Left), int(detection.Top), 			int(detection.Right), int(detection.Bottom)
                cv2.rectangle(frame, (left, top), (right, bottom), (0,255,255), 2)
                cv2.imwrite("banana.jpeg", frame)
                if banFlag == 0:
                    break;
                banFlag = 1
        else: 
                banFlag = 3

    if botFlag == 1:
        i += 1
        if(i == 5 and numBot > 0):
           print("bottle here")
           main.send_signal("bottle",1)
           main.addImage("bottle.jpeg")
        botFlag = 0

    if botFlag == 3:
        if(i > 20 and numBot == 0):
           print("bottle not here")
           main.send_signal("bottle", 0)
           i = 0
        botFlag = 0
    
    if appFlag == 1:
        j += 1
        if(j == 5 and numApp > 0):
           print("apple here")
           main.send_signal("apple",1)
           main.addImage("apple.jpeg")
        appFlag = 0

    if appFlag == 3:
        if(j > 20 and numApp == 0):
           print("apple not here")
           main.send_signal("apple",0)
           j = 0
        appFlag = 0
    
    if banFlag == 1:
        k += 1
        if(k == 5 and numBan > 0):
           print("banana here")
           main.send_signal("banana",1)
           main.addImage("banana.jpeg")
        banFlag = 0

    if banFlag == 3:
        if(k > 20 and numBan == 0):
           print("banana not here")
           main.send_signal("banana",0)
           k = 0
        banFlag = 0

    cv2.imshow('OUTPUT', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

vidCap.release()
cv2.destroyAllWindows()
