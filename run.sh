#!/bin/bash

sudo echo 14 > /sys/class/gpio/unexport
sudo echo 15 > /sys/class/gpio/unexport
sudo echo 18 > /sys/class/gpio/unexport
sudo echo 23 > /sys/class/gpio/unexport

sudo echo 23 > /sys/class/gpio/export
sudo echo out > /sys/class/gpio/gpio23/direction
sudo echo 14 > /sys/class/gpio/export
sudo echo out > /sys/class/gpio/gpio14/direction
sudo echo 15 > /sys/class/gpio/export
sudo echo out > /sys/class/gpio/gpio15/direction
sudo echo 18 > /sys/class/gpio/export
sudo echo out > /sys/class/gpio/gpio18/direction


python ./src/main.py