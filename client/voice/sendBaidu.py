#coding=utf-8
import urllib,urllib2

import requests
import json
from requests import Request,Session

from file_to_base64 import file_to_base64
import os


apiKey ="OhqSXEmuAopiyr7LMWXcDs73"
secretKey = "IMfvWF4ygtxIzmt5lT5qp0EimSIkqbb2"


getTokenURL = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials" + "&client_id=" + apiKey + "&client_secret=" + secretKey


f = urllib.urlopen(getTokenURL)


try:
	access_token =  eval(f.read())['access_token']
except:
	print " Try to refresh your auth code"
	exit(0)	


serverUrl = "http://vop.baidu.com/server_api" 

cuid = "voiceTest"

body = ""
content_length = 0
file_len = os.path.getsize('cmd.wav')
print file_len
try:	
	body = file_to_base64("cmd.wav")
	if body == None:
		raise Exception
except:
	print "Change file_to_base64 failed"	
	exit(0)

headers = {
	"content-type":"application/json",
	"charset" : "utf-8",
}

data_json = {
	"format": "wav",
	"rate"  : 16000,
	"channel": 1,
	"len" : file_len,
	"speech": body,
	"cuid":cuid,
	"token":access_token,
}

r = requests.post(serverUrl,headers = headers, data = json.dumps(data_json))

text = r.json()['result'][0].encode('utf-8')

print text

if '短信' in text:
	print "ok" 
