#!/usr/bin/env python
# encoding: utf-8

import gpio
import time

R,G,B=14,15,18
Anode=23

class RGB(object):
	"""docstring for RGB"""
	def __init__(self):
		super(RGB, self).__init__()

	def reset(anode,red,green,blue):
		gpio.setup(anode,'out')
		gpio.set(anode,0)
		gpio.setup(red,'out')
		gpio.set(red,0)
		gpio.setup(green,'out')
		gpio.set(green,0)
		gpio.setup(blue,'out')
		gpio.set(blue,0)


	def set_color(color):
		gpio.setup(Anode,'out')
		gpio.set(Anode,1)
		gpio.setup(R,'out')
		gpio.set(R,1)
		gpio.setup(G,'out')
		gpio.set(G,1)
		gpio.setup(B,'out')
		gpio.set(B,1)
		if color == 'red':
			gpio.set(R,0)
		elif color == 'green':
			gpio.set(G,0)
		elif color == 'blue':
			gpio.set(B,0)

		
