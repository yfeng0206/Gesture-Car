# Hand Gesture Controlled Robot through OpenCV and an IoT Webserver "CVcar"
ECE 4180 Final Project (Fall 2021 - Section A)

<img src="https://user-images.githubusercontent.com/78784280/145456514-06a19176-1532-46f3-b22f-5fb9e83ddda6.jpeg" width="850">

# Authors
Feng Yunchu, Faiza Yousuf, Harry Nguyen, Christine Saw

# Table of Contents
- [Overview](README.md#overview)
- [Parts List](README.md#parts-list)
- [Hardware Setups](README.md#hardware-setups)
  - [Vehicle Setup](README.md#vehicle-setup)
  - [Raspberry Pi 4](README.md#pin-connection-of-the-pi)
  - [MBED LPC1768](README.md#pin-connection-of-the-mbed)
- [Table of Commands](README.md#table-of-commands)
- [Instructions](README.md#instructions)
- [Summary Video](README.md#summary-video)
- [Demo Video](README.md#demo-video)
- [Future Improvements](README.md#future-improvements)
- [Final Demo Submission](README.md#final-demo-submission)

# Overview
This project aims to create a hand gesture-controlled car that can recognize hand commands to move and perform four motions (forward, reverse, right turn, left turn). It uses a Pi camera to capture hand gestures, a Raspberry Pi 4 to interface with the Pi camera and translate detected hand gestures into commands that are sent to a server run by an MBED (using a ESP8266 module). Finally, the MBED takes the commands and moves the robot accordingly.

<img src="https://user-images.githubusercontent.com/78784280/145411276-7d4bd055-054c-4d5b-b3a5-7a5d652541ab.png" width="850">

[back to top](README.md#hand-gesture-controlled-robot-through-opencv-and-an-iot-webserver-cvcar)

# Parts List
- Hardware:
  - Raspberry Pi 4 (model B)
  - MBED LPC1768
  - Pi Camera
  - 2 DC motors 
  - Dual H-bridge breakout board 
  - 4 LED lights (and 330 Ohm resistors)
  - Power supply with stable amp (4AA battery pack to power ESP8266 and H-bridge, and power bank to power MBED)
  - ESP8266 Adafruit module

- Software:
  - Languages:  
    - Python 3 - see Handtracking/handtracker_to_Server.py
    - C++ - see Project_Wifi_Config and Project_Wifi_Server
  - Compilers:
    - Thonny - compiler seen in demo for python
    - MBED online compiler
  - Libraries:
    - OpenCV - library for real time computer vision
    - MediaPipe - library for hand modules/hand tracking
    - Motor - MBED library to control DC motors through H-Bridge
  

[back to top](README.md#hand-gesture-controlled-robot-through-opencv-and-an-iot-webserver-cvcar)

# Hardware Setups

## Vehicle Setup
Instructions on how to assemble the vehicle's base build can be found here: https://learn.sparkfun.com/tutorials/assembly-guide-for-redbot-with-shadow-chassis/all

Note that our design does not include the "Nub Caster":

<img src="https://user-images.githubusercontent.com/48961286/145506225-1a25da07-c843-4ff9-9a81-8418eba2676a.png">
  
Its purpose is to balance the robot so it's always parallel to the floor; however, it frequently scraped against the ground and interferred with the intended trajectory of the robot's movements, and resulted in slanted motions.

### To compensate for the robot being off balance, the speeds and durations for each motion is as follows (found in Project_Wifi_Server):
Turns are at full speed and last half a second. Forward and Reverse are at 80% pwm and last five seconds. 
```
void LeftTurn(){
       //left
        led4=1;
        Left.speed(-1.0);
        Right.speed(1.0);
        wait(0.5);
        Left.speed(0.0);
        Right.speed(0.0);
        led4=0;
}
void RightTurn(){
        //right
        led3=1; 
        Left.speed(1.0);
        Right.speed(-1.0);
        wait(0.5);
        Left.speed(0.0);
        Right.speed(0.0);
        led3=0;    
    
}

void Forward(){
        //forward
        led1=1;
        Left.speed(0.8);
        Right.speed(0.8);
        wait(5);
        Left.speed(0.0);
        Right.speed(0.0);
        led1=0;
}


void Reverse(){
     //reverse
    led2=1;
    Left.speed(-0.8);
    Right.speed(-0.8);
    wait(5);
    Left.speed(0.0);
    Right.speed(0.0);
    led2=0;
}

```

## Pin Connection of the Pi
<img src="https://user-images.githubusercontent.com/78784280/145406918-eed09443-98ee-4211-9d10-eaa107adf42a.PNG" width="500">

## Pin Connection of the mbed
<img src="https://user-images.githubusercontent.com/78784280/145406927-b24258c0-04cc-4c60-99fb-eeafa61f566d.PNG" width="800">

### The Pi sends data to the mbed over a wifi ESP8266 module (used in Lab 2). A server was established for their connection. In this case, the address is at http://192.168.1.10/ 
<img src="https://user-images.githubusercontent.com/78784280/145407604-073c9c47-6015-49ab-a1c0-314970d15053.png" width="500">


[back to top](README.md#hand-gesture-controlled-robot-through-opencv-and-an-iot-webserver-cvcar)

# Table of Commands
The number of fingers held up by the user will determine the robot’s movement.

| Number of fingers held up  | Robot movement |
| ------------- | ------------- |
| 0  | Hand not Detected - Alerts Users that their hand is not visible  |
| 1  | Forward   |
| 2  | Reverse   |
| 3  | Right Turn|
| 4  | Left Turn |
| 5  | Hand Detected - Alerts Users that their hand is visible and gestures will be tracked |

When handtracker_to_Server.py is run, red dots appear on the hand when the hand is recognized. Also, the camera view has prompts to alert the user what is happening. In this case, the hand is now visible and the user is ready to make a gesture.
![4180HandCapture](https://user-images.githubusercontent.com/48961286/145516818-f8dc7ac0-6c26-4e83-aff4-f62e1844fe4b.PNG)


[back to top](README.md#hand-gesture-controlled-robot-through-opencv-and-an-iot-webserver-cvcar)

# Instructions
After obtaining the hardware, follow the instructions that came with each part to setup the environment.

- Raspberry Pi 4
  - https://www.raspberrypi.com/documentation/computers/getting-started.html

- Pi Camera
  - https://projects.raspberrypi.org/en/projects/getting-started-with-picamera

- OpenCV tutorial for hand-gesture detection
  - https://google.github.io/mediapipe/solutions/hands.html

- Hardware setup
  - Build the robot and setup the Pi and mbed connections following instructions in [Hardware Setups](README.md#hardware-setups)

- Running the code
  - MBED LPC1768
    - Compile the *Project_Wifi_Config* program into the mbed to ensure the ESP8266 is connected to the wifi network. **Link to repo**: https://os.mbed.com/users/fyousuf6/code/ECE4180_WirelessGestureControlCar_CVcar_/
    - Compile the *Project_Wifi_Server* program into the mbed. This step initializes the server that connects the Pi and mbed and allows the mbed to receive messages from the Pi. **Link to repo**: https://os.mbed.com/users/fyousuf6/code/ECE4180-WirelessGestureControlCar_CVcar_/rev/ce3305cf50b4/
  - Raspberry Pi 4
    - Download the *Handtracking* files to a directory and open terminal in that directory.
    - Run the hand gesture detection program ```python3 handtracker_to_Server.py``` or in the IDE
    - NOTE: Running handtracker_to_Server.py in an IDE results in smoother framerate
  

[back to top](README.md#hand-gesture-controlled-robot-through-opencv-and-an-iot-webserver-cvcar)

# Summary Video

https://www.youtube.com/watch?v=mAgygFNm7wE

The video above summarizes the basic functionality of the 3 programs needed to control the car:
1. **handtracker_to_Server.py**
  - located in Handtracking folder on Github, must be run in IDE, in our case, we use Thonny
  - must share a directory with the "Fingers" folder, as the program references the five images to run the MediaPipe hand module (Handtracking/Fingers)
  - uses OpenCV to process images
  - relies on MediaPipe’s handmodule, which sections the hand into 20 distinct points, to read hand gestures
  - the main function handles the OpenCV/Computer Vision and handtracking components of project
  - External LED's connected through GPIO, see [Pin Connection of the Pi](README.md#pin-connection-of-the-pi), are also turned on according to how many fingers are visible (ex. three fingers up result in LEDs 1, 2, and 3 truning on)
  - draws the camera window, tracks current gesture, then sends the number of finger’s held up to the MBED through the send_command() function.
  ```
  def send_command(data_in):
    API_ENDPOINT='http://192.168.1.10/'## ESP8266 server address
    data ={'command': data_in}##will send 'command==#' to server (only numbers 1,2,3, and 4 will result in motion)
    
    try:
        requests.post(url = API_ENDPOINT, data = data)##posts data to API_ENDPOINT address
    except Exception:
        pass
    pass
  ```
  - To avoid bombarding the server with commands, the current gesture and previous gesture are tracked, and a command is only sent when they do not equal each other (i.e. when   the user makes a new gesture
  ```
  ##will only update server if the gesture has changed (ensures server isn't bombarded with messages)    
               if previousGesture!=currentGesture:
                   send_command(str(int(currentGesture)))
                   previousGesture=currentGesture

  ```
2. **Project_Wifi_Config**
  - located in both MBED repo and Github
  - download the program to the MBED to ensure the ESP8266 is connected to your wifi network
  - terminal will display the IP address of the server (change the address in handetracker_to_Server.py accordingly)
  - the SSID and password of the network is saved to the ESP8266, may need to be rerun if the wifi disconnects
  - below is a screenshot of the MBED terminal (through PuTTY), showing the ESP8266 is configured
  ![Project_Wifi_Config_Terminal](https://user-images.githubusercontent.com/48961286/145517270-cdb9c3b7-ba24-4635-a268-82000da41022.PNG)

3. **Project_Wifi_Server**
  - located in both MBED repo and Github
  - initializes server, so it is ready to interpret messages from the Pi into motion
  - built in LEDs on the MBED are switched on when the corresponding motion occures (see gestures 1-4 in [Table of Commands](README.md#table-of-commands))
  - below is a screenshot of the MBED terminal (through PuTTY) showing the server is online and ready to receive the Pi's commands
  ![Creation of Server](https://user-images.githubusercontent.com/48961286/145517346-c388413e-a316-42bd-9998-693b79ddc301.PNG)



[back to top](README.md#hand-gesture-controlled-robot-through-opencv-and-an-iot-webserver-cvcar)

# Demo Video

Short demo video of the robot's operations: https://www.youtube.com/watch?v=9tCQLGX4CgQ&feature=emb_logo

[back to top](README.md#hand-gesture-controlled-robot-through-opencv-and-an-iot-webserver)

# In Class Presentation
https://docs.google.com/presentation/d/1Q2dnvHehjRTc9gWVgPLmKQxMYCxeDP0f9oN5fYWSIe4/edit?usp=sharing
[back to top](README.md#hand-gesture-controlled-robot-through-opencv-and-an-iot-webserver)

# Future Improvements
- Include a wider range of robot motions 
- Be able to control speed with gestures
- Detection of gestures beyond number of fingers
- Add a secondary camera to the mobile robot for live video as it moves
- Add more detail to the server webpage, such as what command is currently being executed
- Find method for more reliable wifi connection

[back to top](README.md#hand-gesture-controlled-robot-through-opencv-and-an-iot-webserver-cvcar)

