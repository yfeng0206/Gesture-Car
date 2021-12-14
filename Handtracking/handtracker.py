import mediapipe
import time
import cv2
import os
from gpiozero import LED
from time import sleep

import requests
##import paho.mqtt.client as mqtt

led1 = LED(16)
led2 = LED(20)
led3 = LED(21)
led4 = LED(26)



##OPENCV drawing and hand module
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands





cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
tipID=[4,8,12,16,20]
totalfinger = 0
cTime = 0
pTime = 0
count=0
overlay = []
mylist=os.listdir("/home/pi/Desktop/Handtracking/Fingers")
for num in range(1,6):
    image = cv2.imread(f'/home/pi/Desktop/Handtracking/Fingers/{num}.jpeg')
    overlay.append(image)


with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.70, min_tracking_confidence=0.7, max_num_hands=2) as hands:

     while True:
           ret, frame = cap.read()
           ix,iy,iz = overlay[0].shape
           #frame[0:ix,0:iy] = overlay[0]
           frame = cv2.flip(frame,-1)
           flipped = cv2.flip(frame, flipCode = -1)
           frame1 = cv2.resize(flipped, (640, 480))
           results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
           handlist = []
           totalfinger = 0
           if results.multi_hand_landmarks != None:
              for handLandmarks in results.multi_hand_landmarks:
                  for id, lm in enumerate(handLandmarks.landmark):
                      h, w, c = frame1.shape
                      cx, cy = int(lm.x*w), int(lm.y *h)
                      handlist.append([id,cx,cy])
                  #print(handlist)
                  opened = []
                  
                  #thumb
                  if(handlist[tipID[0]][1]>handlist[tipID[0]-1][1]):
                      opened.append(1)
                  else:
                      opened.append(0)
                  
                  
                  
                  for id in range(1,5):
                      if(handlist[tipID[id]][2]<handlist[tipID[id]-2][2]):
                          opened.append(1)
                      else:
                          opened.append(0)
                  
                  totalfinger = opened.count(1)
                  print(opened)        
                  drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
                  
           
           cTime = time.time()
           fps = 1/(cTime-pTime)
           pTime = cTime
           cv2.putText(frame1,"fps: "+str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
           cv2.putText(frame1, str(totalfinger),(10,150),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
           
           if totalfinger >= 4:
               led1.on()
               led2.on()
               led3.on()
               led4.on()
               
           elif totalfinger == 3:
               led1.on()
               led2.on()
               led3.on()
               led4.off()
               
           elif totalfinger == 2:
               led1.on()
               led2.on()
               led3.off()
               led4.off()
               
           elif totalfinger == 1:
               led1.on()
               led2.off()
               led3.off()
               led4.off()
               
           else:
               led1.off()
               led2.off()
               led3.off()
               led4.off()
           cv2.imshow("Frame", frame1);
           key = cv2.waitKey(1) & 0xFF
           if key == ord("q"):
              break
