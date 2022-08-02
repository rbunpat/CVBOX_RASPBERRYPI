import os
import cv2
import sys
import time
import json
import argparse
import logging
import requests
import numpy as np
import RPi.GPIO as GPIO  #import raspberry pi gpio library
from cv2 import *
from imutils.video import Videostream
from mlx90614 import MLX90614 #get mlx90614 library from https://pypi.org/project/PyMLX90614/
from smbus import SMbus #i2c shit
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD #sudo pip install rpi_lcd https://github.com/bogdal/rpi-lcd https://www.electroniclinic.com/raspberry-pi-16x2-lcd-i2c-interfacing-and-python-programming/

lcd = LCD()

camID = 0
cam = VideoCapture(camID)

relayPin = 'yourrelaypinhere'
trigPin = "yourtriggerpinhere"
echoPin = "yourechopinhere"
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(relayPin, GPIO.OUT)

tempSensor = MLX90614(bus, address='TEMP SENSOR THINGY I2C ADDRESS')
tempAMB = tempSensor.get_ambient_temp()
tempOBJ = tempSensor.get_object_temp()

def checktemp():
    if (tempOBJ > 29 and tempOBJ < 37.4):
        lcd.text('normal temp')
        dispenseALC(0.5)
        time.sleep(0.5)
        lcd.clear()
        lcd.text('Scan Temperature')
    elif (tempOBJ >= 37.5 and tempOBJ < 40):
        secondscan = tempSensor.get_object_temp()
        if (secondscan > 30 and secondscan < 37.5):
            lcd.text('normal temp')
            dispenseALC(0.5)
            time.sleep(0.5)
            lcd.clear()
            lcd.text("Scan Temperature")
        elif (secondscan > 37.5 and secondscan < 40):
            lcd.text('high temp')
            time.sleep(0.5)
            lcd.clear()
            lcd.text('Scan Temperature')
        elif (secondscan > 40 or secondscan < 30):
            lcd.text('rekt')
            time.sleep(0.5)
            lcd.clear()
            lcd.text("Scan Temperature")
    else:
        print('temp is more than 40 or less tham 30')

def dispenseALC(dsptime):
    GPIO.output(relayPin, HIGH)
    time.sleep(dsptime)
    GPIO.output(relayPin, LOW)

def sendtoLine(message):
    url = 'https://notify-api.line.me/api/notify'
    token = 'Ac8UgXdvRTq0uw6LT9SbTaqvLpPaPOTgcxkS2UK4rle'
    img = {'imageFile': open('picturefilenamehere.png','rb')}
    data = {'message': message}
    headers = {'Authorization':'Bearer ' + token}
    session = requests.Session()
    session_post = session.post(url, headers=headers, files=img, data =data)
    print(session_post.text)

def captureIMG():
    result, image = cam.read()
    imwrite("somepicture.png", image)

def calDist():
    GPIO.output(trigPin, True)
    time.sleep(0.00001)
    GPIO.output(trigPin, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(echoPin) == 0:
        StartTime = time.time()
    while GPIO.input(echoPin) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

if __name__ == '__main__':
    try:
        bus = SMbus(1)
        lcd.clear()
        lcd.text('Scan Temperature')
        checktemp()
    except KeyboardInterrupt:
        print('interrupted')
        try:
            lcd.clear()
            GPIO.cleanup()
            cam.release()
            cv2.destroyAllWindows
            bus.close()
            sys.exit(0)
        except:
            os._exit(0)





