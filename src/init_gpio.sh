#!/bin/bash

echo 23 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio23/direction
echo 14 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio14/direction
echo 15 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio15/direction
echo 18 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio18/direction