# -*- coding: utf-8 -*-
#!/usr/bin/env python 

import urllib,urllib2
import requests
import json
from requests import Request,Session
import ConfigParser
import base64
import os

class Baidu(object):
	"""docstring for Baidu"""
	def __init__(self, file_format, audio_file):
		super(Baidu, self).__init__()
		config = ConfigParser.ConfigParser()
		config.read('./config/config.ini')

		self.cuid = config.get('baidu','cuid')
		self.api_key = config.get('baidu','apiKey')
		self.secret_key = config.get('baidu','secretKey')
		self.token_url = config.get('baidu','tokenUrl')
		self.server_url = config.get('baidu','serverUrl')
		self.file_format = file_format
		self.audio_file = audio_file 
		

	def get_token(self):
		get_token_url = self.token_url + "&client_id=" + self.api_key + "&client_secret=" + self.secret_key
		#print get_token_url
		f = urllib.urlopen(get_token_url)
		try:
			access_token =  eval(f.read())['access_token']
		except:
			print " Try to refresh your auth code"
			exit(0)
		return access_token	


	def decode_file(self):
		with open(self.audio_file,"r") as f:
			data = f.read()
			data_base64 = base64.b64encode(data) 
		if data_base64:
			return data_base64
		else:
			print "Failed encode the file to base64"
			return None 

    
	def send_audio(self):
		content_length = 0
		file_len = os.path.getsize(self.audio_file)
		body = self.decode_file()
		access_token = self.get_token()
		data_json = {
			"format" : self.file_format,
			"rate"   : 16000,
			"channel": 1,
			"cuid"   : self.cuid,
			"token"  : access_token,
			"len"    : file_len,
			"speech" : body,
		}

		headers = {
			"content-type":"application/json",
			"charset" : "utf-8",
		}

		r = requests.post(self.server_url, headers = headers, data = json.dumps(data_json))

		return r


	def get_result(self):
		result = self.send_audio()
		print result.text
		#print type(result)
		result = result.json()
		#print type(result)
		if result.get('err_no') == 0:
			text = "".join(result.get('result')).encode('utf-8')
			#print text
		else:
			err_msg = "".join(result.get('err_msg')).encode('utf-8')
			# print "err_no:"+str(err_no)
			#exit(0)

if __name__ == "__main__":
	test = Baidu(file_format = "pcm", audio_file = "../data/cmd.pcm")
	test.get_result()
