#!/usr/bin/python
# coding: utf-8
import cv2 as cv2
import time
import numpy as np
import RPi.GPIO as gpio
gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(12, gpio.OUT)
gpio.setup(16, gpio.OUT)
gpio.setup(18, gpio.OUT) 
gpio.setup(22, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(40, gpio.OUT)
gpio.setup(32, gpio.OUT)
gpio.setup(36, gpio.OUT)
gpio.setup(38, gpio.OUT)
gpio.output(7, True) #Motor A - Rasp 1
gpio.output(11, True) #Motor A - Rasp 2
gpio.output(12, True) #Motor B - Rasp 1
gpio.output(16, True) #Motor B - Rasp 2

def reverse():
# Motor 1
 gpio.output(13, False)
 gpio.output(15, True)
# Motor 2
 gpio.output(18, True)
 gpio.output(22, False)
# Motor 1
 gpio.output(32, False)
 gpio.output(36, True)
# Motor 2
 gpio.output(38, True)
 gpio.output(40, False)

	
def forward():
 gpio.output(13, True)
 gpio.output(15, False)
# Motor 2
 gpio.output(18, False)
 gpio.output(22, True)
# Motor 1
 gpio.output(32, True)
 gpio.output(36, False)
# Motor 2
 gpio.output(38, False)
 gpio.output(40, True)
def stop():
# Motor 1
 gpio.output(18, False)
 gpio.output(22, False)
# Motor 2
 gpio.output(13, False)
 gpio.output(15, False)
# Motor 1
 gpio.output(32, False)
 gpio.output(36, False)
# Motor 2
 gpio.output(38, False)
 gpio.output(40, False)

def right():
 gpio.output(13, True)
 gpio.output(15, False)
 gpio.output(18, True)
 gpio.output(22, False)


def left():
 gpio.output(13, False)
 gpio.output(15, True)
 gpio.output(18, False)
 gpio.output(22, True)
Hmin = 42
Hmax = 92
Smin = 62
Smax = 255
Vmin = 63
Vmax = 235


#Padrão RED
#Hmin = 0
#Hmax = 179 
#Smin = 131
#Smax = 255
#Vmin = 126
#Vmax = 255


rangeMin = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMax = np.array([Hmax, Smax, Vmax], np.uint8)


def processamento(entrada):
     imgMedian = cv2.medianBlur(entrada,1)
     imgHSV = cv2.cvtColor(imgMedian,cv2.COLOR_BGR2HSV)	
     imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
     imgErode = cv2.erode(imgThresh, None, iterations = 3)
     return imgErode


capture = cv2.VideoCapture(0)

largura = 160
altura = 120

minArea = 50 

centroy = altura/2


may = altura/5 

if capture.isOpened():
  capture.set(cv2.CAP_PROP_FRAME_WIDTH, largura)
  capture.set(cv2.CAP_PROP_FRAME_HEIGHT, altura)

  
while True:
    ret, entrada = capture.read()
    imagem_processada = processamento(entrada)
    moments = cv2.moments(imagem_processada, True)
    area = moments['m00']
    if moments['m00'] >= minArea:
     x = moments['m10'] / moments['m00']
     y = moments['m01'] / moments['m00']
     cv2.circle(entrada, (int(x), int(y)), 5, (0, 255, 0), -1)
     if(area<=120):
      reverse()
     elif(area>=600):
      forward()
     else:
      stop()	

	
