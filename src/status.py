#!/usr/bin/env python
# encoding: utf-8

import RPi.GPIO
import time

R,G,B=15,18,14

RPi.GPIO.setmode(RPi.GPIO.BCM)

RPi.GPIO.setup(R, RPi.GPIO.OUT)
RPi.GPIO.setup(G, RPi.GPIO.OUT)
RPi.GPIO.setup(B, RPi.GPIO.OUT)

pwmR = RPi.GPIO.PWM(R, 70)
pwmG = RPi.GPIO.PWM(G, 70)
pwmB = RPi.GPIO.PWM(B, 70)

pwmR.start(0)
pwmG.start(0)
pwmB.start(0)

try:

	t = 0.4
	#while True:
		# 红色灯全亮，蓝灯，绿灯全暗（红色）
	pwmR.ChangeDutyCycle(0)
	pwmG.ChangeDutyCycle(100)
	pwmB.ChangeDutyCycle(100)
	time.sleep(t)
		
		# # 绿色灯全亮，红灯，蓝灯全暗（绿色）
		# pwmR.ChangeDutyCycle(100)
		# pwmG.ChangeDutyCycle(0)
		# pwmB.ChangeDutyCycle(100)
		# time.sleep(t)
		
		# # 蓝色灯全亮，红灯，绿灯全暗（蓝色）
		# pwmR.ChangeDutyCycle(100)
		# pwmG.ChangeDutyCycle(100)
		# pwmB.ChangeDutyCycle(0)
		# time.sleep(t)
		

except KeyboardInterrupt:
	pass

pwmR.stop()
pwmG.stop()
pwmB.stop()

RPi.GPIO.cleanup()