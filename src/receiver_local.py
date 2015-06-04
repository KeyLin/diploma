#!/usr/bin/env python
#coding:utf8

import pika
import sys
import os
import time
from record_play import RecordAndPlay
from memo import SendMessage

def action(body):
    MyMemo = SendMessage()
    words=body.split(',')
    print words[0]
    while MyMemo.send_mail(words[0],'')==False:
        print ".",
        time.sleep(3)
        pass
    print "Send Mail Successfully"
    pass


def connect(ip, exchange_name, binding_keys):
    credentials = pika.PlainCredentials('test', 'test')
    parameters =  pika.ConnectionParameters(ip, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_name,
                             type='topic')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    for binding_key in binding_keys:
        channel.queue_bind(exchange=exchange_name,
                           queue=queue_name,
                           routing_key=binding_key)

    print ' [*] Waiting for message. To exit press CTRL+C'

    def callback(ch, method, properties, body):
        action(body)
        print " [x] %r:%s" % (method.routing_key, body.decode('utf8'),)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()


def main():
    keys = sys.argv[1:]
    if not keys:
        print >> sys.stderr, "Usage: %s [binding_key]..." % (sys.argv[0],)
        sys.exit(1)
    connect(ip='localhost',exchange_name='raspberry',binding_keys=keys)

if __name__ == '__main__':
    main()

# sudo rabbitmqctl add_user test test
# sudo rabbitmqctl set_user_tags test administrator
# sudo rabbitmqctl set_permissions -p / test ".*" ".*" ".*"
