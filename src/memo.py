#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import smtplib
import urllib2
import json
import ConfigParser  
from email.mime.text import MIMEText

class SendMessage(object):
    """docstring for SendMessage"""
    def __init__(self):
        super(SendMessage, self).__init__()
        config = ConfigParser.ConfigParser()
        config.read('./config/config.ini')

        self.mail_sender = config.get('Mail','mail_sender')
        self.mail_pass = config.get('Mail','mail_pass')
        self.mail_host = config.get('Mail','mail_host')
        self.mail_receivers = config.get('Mail','mail_receivers')
  
    def send_mail(self,subject,content):  
        sender="memo"+"<"+self.mail_sender+">"  
        msg = MIMEText(content,_subtype='plain',_charset='utf-8')  
        msg['Subject'] = subject  
        msg['From'] = sender  
        msg['To'] = self.mail_receivers 
        try:  
            server = smtplib.SMTP()  
            server.connect(self.mail_host)  
            server.login(self.mail_sender, self.mail_pass)
            self.mail_receivers = self.mail_receivers.split(";")
            for receiver in self.mail_receivers:  
                server.sendmail(sender, receiver, msg.as_string())  
            server.close()  
            return True  
        except Exception, e:  
            #print str(e)  
            return False


def main():
    test = SendMessage()

    message = "test"

    print message

    while test.send_mail(message,message)==False:
        print ".",
        time.sleep(3)
        pass
    print "Send Mail Successfully"


if __name__ == '__main__':
    main()
