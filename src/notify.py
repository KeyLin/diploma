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

        self.sms_sender = config.get('SMS','sms_sender')
        self.feixin_pass = config.get('SMS','feixin_pass')
        self.sms_receivers = config.get('SMS','sms_receivers')

        self.mail_sender = config.get('Mail','mail_sender')
        self.mail_pass = config.get('Mail','mail_pass')
        self.mail_host = config.get('Mail','mail_host')
        self.mail_receivers = config.get('Mail','mail_receivers')
  
    def send_mail(self,subject,content):  
        sender="Notify"+"<"+self.mail_sender+">"  
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

    def send_sms(sender,passwd,receivers,message):
        url="http://quanapi.sinaapp.com/fetion.php?u="+sender+"&p="+passwd+"&to="+receivers+"&m="+message
        try:  
            result= json.loads(urllib2.urlopen(url).read())
            if result["result"]==0:
                return True
            else:
                return False  
        except Exception, e:  
            #print str(e)  
            return False


    def time_control(timeLimit):
        #判断文件是否存在
        if os.path.exists('.\\timeRecord.txt') == False:
            f = open('.\\timeRecord.txt', 'w')
            f.close
        #读取文本中记录的日期
        f = open('.\\timeRecord.txt', 'r+')
        f_date = f.readline()
        f.close
        #读取系统日期，并与文本日期进行比对,如果不相等，则清空文件，进行当日初始化
        n_date = time.strftime("%d/%m/%Y") + "\n"
        if f_date != n_date:
            f = open('.\\timeRecord.txt', 'r+')
            f.truncate()
            f.close
            f = open('.\\timeRecord.txt', 'r+')
            f.write((n_date))
            run_time = "0"
            f.write(run_time)
            f.close
            #死循环语句，当且仅当运行时间大于等于限制时间时跳出循环
        while True:
            f = open('.\\timeRecord.txt', 'r+')
            f_date = f.readline()
            run_time = f.readline()
            run = int(run_time)
            time.sleep(60)
            if run < timeLimit:
                run = run + 1
                f.truncate()
                f.close
                f = open('.\\timeRecord.txt', 'r+')
                f.write(f_date)
                run_time = str(run)
                f.write(run_time)
                f.close
            else:
                break

        while send_sms(sms_sender,feixin_pass,sms_receivers,"今天的上机时间用完了")==False:
            print ".",
            time.sleep(3)
            pass

def main():
    test = SendMessage()

    message = "XXX在" + time.strftime('%H:%M',time.localtime(time.time())) + "打开了电脑"

    print message

    # while test.send_sms(message)==False:
    #     print ".",
    #     time.sleep(3)
    #     pass
    # print "Send SMS Successfully"

    while test.send_mail(message,message)==False:
        print ".",
        time.sleep(3)
        pass
    print "Send Mail Successfully"


if __name__ == '__main__':
    main()
