#!/usr/bin/env python
#coding=utf8
import pika

route_dic={u'音乐':'music.',u'备忘录':'mail.'}

class Emit(object):
 	"""docstring for Emit"""
 	def __init__(self, ip = 'localhost', port = 5672, EXCHANGE = 'raspberry', TYPE = 'topic'):
 		super(Emit, self).__init__()
 		self.ip = ip
 		self.port = port
 		self.exchange = EXCHANGE
 		self.type = TYPE

 	def get_route(self,words):
 		for key in words:
 			#print key
 			route = route_dic.get(key)
 			#print route
 			if route != None:
 				return route
 		return 'error'

 	def emit_message(self,message,words):
 		#print message
 		route = self.get_route(words)
 		#print route
 		connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip,self.port))
 		channel = connection.channel()
 		channel.exchange_declare(exchange=self.exchange, type=self.type)
 		content = message+','+','.join(words)
 		#print type(content)
 		#print words
 		channel.basic_publish(exchange=self.exchange,routing_key=route,body=content)
 		#print content
 		connection.close()

if __name__ == '__main__':
	test = Emit()
	test.emit_message(u'播放音乐',[u'音乐',u'备忘录'])
	test.emit_message(u'打开备忘录',[u'备忘录',u'音乐'])