

import RPi.GPIO as GPIO    
import time
import numpy as np
import cv2

#set the GPIO pins of raspberry pi.
    GPIO.setmode (GPIO.BCM)
    GPIO.setwarnings (False)
#enable
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
#setting the GPIO pin as Output
    GPIO.setup (24, GPIO.OUT)
    GPIO.setup (23, GPIO.OUT)
    GPIO.setup (27, GPIO.OUT)
    GPIO.setup (22, GPIO.OUT)
#GPIO.PWM( pin, frequency ) it generates software PWM
    PWMR = GPIO.PWM (24, 100)
    PWMR1 = GPIO.PWM (23, 100)
    PWML = GPIO.PWM (27, 100)
    PWML1 = GPIO.PWM (22, 100)
#Starts PWM at 0% dutycycle
    PWMR.start (0)
    PWMR1.start (0)
    PWML.start (0)
    PWML1.start (0)
#enable pins of the motor
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)

while(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1) # Flip camera vertically since camera is actually fliped in our fixation
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    blur=cv2.GaussianBlur(gray,(5,5),0)#blur the grayscale image
    ret,th1 = cv2.threshold(blur,35,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)#using threshold remave noise
    ret1,th2 = cv2.threshold(th1,127,255,cv2.THRESH_BINARY_INV)# invert the pixels of the image frame
    im2, contours, hierarchy = cv2.findContours(th2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #find the contours
    cv2.drawContours(frame,contours,-1,(0,255,0),3)
    cv2.imshow('frame',frame) #show video
    cnt = contours[0]
    #for cnt in contours:
       #if cnt is not None:
    area = cv2.contourArea(cnt)# find the area of contour
        #if area>=500 :
            # find moment and centroid
    M = cv2.moments(cnt)
    if M["m00"] !=0:
        
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    else:
        cx, cy = 0, 0
    
    if cx<=270:
        l=(cx*100/320)
        PWMR.start (0)
        PWML.start (0)
        PWMR1.ChangeDutyCycle (80)
        PWML1.ChangeDutyCycle (0)
        time.sleep(0.5)
                
    elif cx>=370:
        r=((640-cx)*100/320)
        PWMR.start (0)
        PWML.start (0)
        PWMR1.ChangeDutyCycle (0)
        PWML1.ChangeDutyCycle (80)
        time.sleep(0.5)
               
    elif cx>270 and cx<370:
        PWMR.start (0)
        PWML.start (0)
        PWMR1.ChangeDutyCycle (80)
        PWML1.ChangeDutyCycle (80)
        time.sleep(0.5)
                
    else:
        PWMR1.start (0)
        PWML1.start (0)
        PWMR.ChangeDutyCycle (00)
        PWML.ChangeDutyCycle (00)
        time.sleep(0.5)
                

            
            
    PWMR.start (0)
    PWMR1.start (0)                 
    PWML.start (0)                 
    PWML1.start (0)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
cap.release()
cv2.destroyAllWindows() 
            
