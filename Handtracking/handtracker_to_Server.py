import mediapipe
import time
import cv2
import os
from gpiozero import LED
from time import sleep
import requests

##identifying led's
led1 = LED(16)
led2 = LED(20)
led3 = LED(21)
led4 = LED(26)



def send_command(data_in):
    API_ENDPOINT='http://192.168.1.10/'## ESP8266 server address
    data ={'command': data_in}##will send 'command==#' to server (only numbers 1,2,3, and 4 will result in motion)
    
    try:
        requests.post(url = API_ENDPOINT, data = data)##posts data to API_ENDPOINT address
    except Exception:
        pass
    pass

def main():
    drawingModule = mediapipe.solutions.drawing_utils
    handsModule = mediapipe.solutions.hands ##will define handmodule, to later determine handmodule parameters (see line 37)
    cap = cv2.VideoCapture(0)##defines WebCam 0 (can choose from different webcams with number parameter)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    tipID=[4,8,12,16,20]##id point of finger tips (4=thumb, 8=index, 12=middle, 16=ring, 20=pinky)
    ##initializes totalfingers seen
    totalfinger = 0
    cTime = 0 ##current Time
    pTime = 0 ##previous Time
    count=0
    currentGesture = 0##track current gesture
    previousGesture = 0##track previous gesture
    overlay = []
    mylist=os.listdir("/home/pi/Desktop/Handtracking/Fingers")
    for num in range(1,6):
        image = cv2.imread(f'/home/pi/Desktop/Handtracking/Fingers/{num}.jpeg')##references 5 fingers images
        overlay.append(image)


    with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.70, min_tracking_confidence=0.7, max_num_hands=2) as hands:
    ##static_image_mode=False (detects based on tracking confidence level), detection_confidence (if below 70%, will try to detect again), tracking_confidence(if below 70%, will run detection again), max number of hands is 2 
         while True:
               ret, frame = cap.read()
               ix,iy,iz = overlay[0].shape
               #frame[0:ix,0:iy] = overlay[0]
               frame = cv2.flip(frame,-1)
               flipped = cv2.flip(frame, flipCode = -1)
               frame1 = cv2.resize(flipped, (640, 480))##draws camera window
               results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))##processing image
               handlist = []
               totalfinger = 0
               if results.multi_hand_landmarks != None:##if a hand is visible
                  for handLandmarks in results.multi_hand_landmarks:##tracks results/points of each hand in handLandmarks object
                      for id, lm in enumerate(handLandmarks.landmark):
                          h, w, c = frame1.shape
                          cx, cy = int(lm.x*w), int(lm.y *h)
                          handlist.append([id,cx,cy])##pairs hand point with its x and y cooridinates
                      opened = []##creates array for fingers indexes (ex: Right hand with index finger up is [0,1,0,0,0])
                  
                      #thumb hardcoding
                      if(handlist[tipID[0]][1]>handlist[tipID[0]-1][1]):
                          opened.append(1)
                      else:
                          opened.append(0)
                  
                  
                  
                      for id in range(1,5):
                          if(handlist[tipID[id]][2]<handlist[tipID[id]-2][2]):
                              opened.append(1)
                          else:
                              opened.append(0)
                  
                      totalfinger = opened.count(1)##total "opened" or held open fingers
                      
                      ##print(opened)        
                      drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)##draws connections between the 20 points of hand
                  
           
               cTime = time.time()##creates current time
               currentGesture=totalfinger
               fps = 1/(cTime-pTime)## fps is 1/(current time - previous time)
               pTime = cTime##set previous time equal to current time
               #previousGesture=currentGesture
               cv2.putText(frame1,"fps: "+str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)##displays frame rate 
               cv2.putText(frame1, str(totalfinger),(10,150),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)##displays fingers visible
               
           
               if totalfinger == 5:
                   print(5)
                   cv2.putText(frame1,"Ready for Gestures", (10,230),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
               elif totalfinger == 4:
                   print(4)
                   led1.on()
                   led2.on()
                   led3.on()
                   led4.on()
                   cv2.putText(frame1,"Left Turn", (10,230),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
                   
               elif totalfinger == 3:
                   print(3)
                   led1.on()
                   led2.on()
                   led3.on()
                   led4.off()
                   cv2.putText(frame1,"Right Turn", (10,230),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
                   
               elif totalfinger == 2:
                   print(2)
                   led1.on()
                   led2.on()
                   led3.off()
                   led4.off()
                   cv2.putText(frame1,"Reverse", (10,230),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
                   
               elif totalfinger == 1:
                   print(1)
                   led1.on()
                   led2.off()
                   led3.off()
                   led4.off()
                   cv2.putText(frame1,"Forward", (10,230),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
                   
               else:
                   print(0)
                   cv2.putText(frame1,"Hand Not Visible", (10,230),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
                   led1.off()
                   led2.off()
                   led3.off()
                   led4.off()                   
                   
               ##will only update server if the gesture has changed (ensures server isn't bombarded with messages)    
               if previousGesture!=currentGesture:
                   send_command(str(int(currentGesture)))
                   previousGesture=currentGesture

               cv2.imshow("Frame", frame1);
               key = cv2.waitKey(1) & 0xFF
               if key == ord("q"):
                  break
                
if __name__ == "__main__":
    main()
