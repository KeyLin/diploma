#!/bin/python


import socket

HOST = "192.168.122.1"
PORT = 50007


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((HOST,PORT))
s.sendall("hello,world")
data = s.recv(1024)
s.close()
print "Received",repr(data)

