#!/bin/python


import base64

def file_to_base64(FILE_NAME):
	with open(FILE_NAME,"r") as f:
		data = f.read()
		
		data_base64 = base64.b64encode(data) 
	if data_base64:
		print "Succeed"
		print len(data_base64)
		return data_base64
	else:
		print "Failed"
		return None 

if __name__ == "__main__":
	file_to_base64("test.pcm")
