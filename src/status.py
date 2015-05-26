#!/usr/bin/env python
# encoding: utf-8

os.system
import time

R,G,B=14,15,18
Anode=23

def pin_init():
	os.system('echo 23 /sys/class/gpio/export')
	os.system('echo out /sys/class/gpio/gpio23/direction')
	os.system('echo 14 /sys/class/gpio/export')
	os.system('echo out /sys/class/gpio/gpio14/direction')
	os.system('echo 15 /sys/class/gpio/export')
	os.system('echo out /sys/class/gpio/gpio15/direction')
	os.system('echo 15 /sys/class/gpio/export')
	os.system('echo out /sys/class/gpio/gpio18/direction')

def set_color(color):
	if color=='red':
		os.system('echo 1 /sys/class/gpio/gpio23/value')
		os.system('echo 0 /sys/class/gpio/gpio14/value')
		os.system('echo 1 /sys/class/gpio/gpio15/value')
		os.system('echo 1 /sys/class/gpio/gpio18/value')

	if color=='green':
		os.system('echo 1 /sys/class/gpio/gpio23/value')
		os.system('echo 1 /sys/class/gpio/gpio14/value')
		os.system('echo 0 /sys/class/gpio/gpio15/value')
		os.system('echo 1 /sys/class/gpio/gpio18/value')

	if color=='blue':
		os.system('echo 1 /sys/class/gpio/gpio23/value')
		os.system('echo 1 /sys/class/gpio/gpio14/value')
		os.system('echo 1 /sys/class/gpio/gpio15/value')
		os.system('echo 0 /sys/class/gpio/gpio18/value')

	# gpio.set(Anode,1)
	# gpio.setup(R,'out')
	# gpio.set(R,1)
	# gpio.setup(G,'out')
	# gpio.set(G,1)
	# gpio.setup(B,'out')
	# gpio.set(B,1)
	# if color == 'red':
	# 	gpio.set(R,0)
	# elif color == 'green':
	# 	gpio.set(G,0)
	# elif color == 'blue':
	# 	gpio.set(B,0)

if __name__ == '__main__':
	set_color(color='red')
	time.sleep(3)
	set_color(color='green')
	time.sleep(3)
	set_color(color='blue')
	time.sleep(3)
	reset()
		
