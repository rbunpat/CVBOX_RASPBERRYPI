import os
import sys
import time
import json
import logging
import requests
import numpy as np
import RPi.GPIO as GPIO 
from cv2 import *
from mlx90614 import MLX90614 #get mlx90614 library from https://pypi.org/project/PyMLX90614/
from smbus import SMbus #i2c shit

camID = 0
cam = VideoCapture(camID)

trigPin = "yourtriggerpinhere"
echoPin = "yourechopinhere"
GPIO,setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

tempSensor = MLX90614(bus, address='TEMP SENSOR THINGY I2C ADDRESS')
tempAMB = tempSensor.get_ambient_temp()
tempOBJ = tempSensor.get_object_temp()

def themainthing():
    print('do something')

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
        themainthing()
    except KeyboardInterrupt:
        print('interrupted')
        try:
            GPIO.cleanup()
            cam.release()
            bus.close()
            sys.exit(0)
        except:
            os._exit(0)
