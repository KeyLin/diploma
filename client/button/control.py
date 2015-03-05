#!/bin/python


from time import sleep
import RPi.GPIO as GPIO
import os


inputPIN = 7 
outputPIN =25
GPIO.setmode(GPIO.BCM)
GPIO.setup(inputPIN,GPIO.IN)
GPIO.setup(outputPIN,GPIO.OUT)


while True:
	if GPIO.input(inputPIN) == False:
		#On	
		os.system('bash ../voice/record.sh')
		break
	else:
		#Off
		pass
