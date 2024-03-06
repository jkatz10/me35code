import numpy as np
import cv2
from picamera2 import Picamera2
from libcamera import controls
import time
import RPi.GPIO as GPIO

picam2 = Picamera2() # assigns camera variable
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous}) # sets auto focus mode
picam2.start() # activates camera

time.sleep(1) # wait to give camera time to start up

in1 =40
in2 =38
in3 =36
in4 =32
ena =37
enb =15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
GPIO.setup(ena, GPIO.LOW)
GPIO.setup(enb, GPIO.LOW)

frequency = 50
pwm1 = GPIO.PWM(ena, frequency)
pwm2 = GPIO.PWM(enb, frequency)
pwm1.start(0)
pwm2.start(0)

def PID(cx):
    kp =0.1
    speed = 17
    target_position = 75
    error = target_position - cx
    correction = error*kp
    return speed + correction

def move_forward(cx):
    speed = PID(cx)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    pwm1.ChangeDutyCycle(speed)
    pwm2.ChangeDutyCycle(speed)
    
#def go_back():
    #GPIO.output(in1, GPIO.LOW)
    #GPIO.output(in2, GPIO.HIGH)
   # GPIO.output(in3, GPIO.LOW)
    #GPIO.output(in4, GPIO.HIGH)
    #pwm1.ChangeDutyCycle(PID(cx))
    #pwm2.ChangeDutyCycle(PID(cx))
    
def turn_right():
    #speed = PID(cx)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(40)



def turn_left():
    #speed = PID(cx)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    pwm1.ChangeDutyCycle(40)
    pwm2.ChangeDutyCycle(0)
    

def stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(0.1)



try:
    while True:
        
        # Display camera input
        image = picam2.capture_array("main")
        cv2.imshow('img',image)
    
        # Crop the image
        centerx = image.shape[1]//2
        centery = image.shape[0]//2
        crop_width = 250
        crop_height = 150
        
        crop_img = image[centery - crop_height//2: centery +crop_height//2, centerx - crop_width//2:centerx +crop_width//2]
        
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    
        # Gaussian blur
        blur = cv2.GaussianBlur(gray,(5,5),0)
    
        # Color thresholding
        input_threshold,comp_threshold = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
    
        # Find the contours of the frame
        contours,hierarchy = cv2.findContours(comp_threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
        # Find the biggest contour (if detected)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c) # determine moment - weighted average of intensities

            if int(M['m00']) != 0:
                cx = int(M['m10']/M['m00']) # find x component of centroid location
                cy = int(M['m01']/M['m00']) # find y component of centroid location
            else:
                print("Centroid calculation error, looping to acquire new values")
                continue
            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1) # display vertical line at x value of centroid
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1) # display horizontal line at y value of centroid
    
            cv2.drawContours(crop_img, contours, -1, (0,255,0), 2) # display green lines for all contours
            
            # determine location of centroid in x direction and adjust steering recommendation
            
            if cx >= 140:
                turn_left()
                print("Turn Right!")
    
            if cx < 140 and cx > 70:
                move_forward(PID(cx))
                print("On Track!")
    
            if cx <= 70:
                turn_right()
                print("Turn Left")

                
        else:
            #go_back()
            print("Go Back! I don't see the line!")
    
        # Display the resulting frame
        cv2.imshow('frame',crop_img)
        
        # Show image for 1 ms then continue to next image
        cv2.waitKey(1)

except KeyboardInterrupt:
    print('All done')
