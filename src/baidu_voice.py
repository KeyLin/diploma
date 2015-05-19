# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib
import urllib2
import requests
import json
from requests import Request, Session
import ConfigParser
import base64
import os


class BaiduVoice(object):

    """docstring for BaiduVoice"""

    def __init__(self, configure):
        super(BaiduVoice, self).__init__()
        config = ConfigParser.ConfigParser()
        config.read(configure)

        self.cuid = config.get('baidu', 'cuid')
        self.api_key = config.get('baidu', 'api_key')
        self.secret_key = config.get('baidu', 'secret_key')
        self.token_url = config.get('baidu', 'token_url')
        self.server_url = config.get('baidu', 'server_url')
        self.access_token = self.get_token()

    def get_token(self):
        get_token_url = self.token_url + "&client_id=" + \
            self.api_key + "&client_secret=" + self.secret_key
        # print get_token_url
        f = urllib.urlopen(get_token_url)
        try:
            access_token = eval(f.read())['access_token']
        except:
            print " Try to refresh your auth code"
            exit(0)
        return access_token

    def get_text(self, file_format, audio_file):

        # if os.path.isfile('audio_file') == False:
        # 	print audio_file
        # 	return "audio_file not exist"

        with open(audio_file, "r") as f:
            data = f.read()
            data_base64 = base64.b64encode(data)

        content_length = 0
        file_len = os.path.getsize(audio_file)
        body = data_base64

        data_json = {
            "format": file_format,
            "rate": 16000,
            "channel": 1,
            "cuid": self.cuid,
            "token": self.access_token,
            "len": file_len,
            "speech": body,
        }

        headers = {
            "content-type": "application/json",
            "charset": "utf-8",
        }

        # print "sending to baidu"
        result = requests.post(
            self.server_url, headers=headers, data=json.dumps(data_json))

        # print result.text
        result = result.json()
        if result.get('err_no') == 0:
            text = "".join(result.get('result')).encode('utf-8')
            # print text
            return text
        else:
            err_msg = "".join(result.get('err_msg')).encode('utf-8')
            return err_msg
            # print "err_no:"+str(err_no)
            # exit(0)


if __name__ == "__main__":
    test = BaiduVoice(configure='../config/config.ini')
    test.get_text(file_format="wav", audio_file="./data/cmd.wav")
