# -*- coding: utf-8 -*-
#!/bin/python

from sphinx import Pocket
from baidu_voice import BaiduVoice
from save_file import SaveFile
from sender import Emit

from ctypes import *

import pyaudio
import time
from Queue import Queue
import threading
import signal
import os,subprocess
import jieba

import sys
reload(sys)
sys.setdefaultencoding('utf8')

#import locale
# locale.setlocale(locale.LC_ALL, '')    # set your locale

ERROR_HANDLER_FUNC = CFUNCTYPE(
    None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)


CHUNK = 1024
RATE = 16000
RECORD_SECONDS = 5
RECORD_CONTROL = int(RATE / CHUNK * RECORD_SECONDS)
FILE_PATH = './data/'
IS_REMOVE = True
IS_EXIT = False


class Producer(threading.Thread):

    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paInt16, channels=1,
                         rate=RATE, input=True, frames_per_buffer=CHUNK)
        stream.start_stream()
        pocket = Pocket(configure='./config/config.ini')
        audio = SaveFile(sample_size=pa.get_sample_size(pyaudio.paInt16))
        start = False
        count = 0
        frames = []
        # print "Producer started"
        while not IS_EXIT:
            #print 'producing'
            time.sleep(0.1)
            # Read the first Chunk from the microphone
            buf = stream.read(CHUNK)
            if buf:
                # print 'hehe'
                pocket.decode_buffer(audio_buf=buf)
                if pocket.get_flag(flag='yes'):
                    start = True
                    count = 0
                    # time.sleep(0.5)
                    pocket.set_flag()

                if count > RECORD_CONTROL:
                    start = False
                    count = 0
                    # time.sleep(0.5)
                    pocket.set_flag()
                    file_name = SaveFile.set_name()
                    audio.save_wav(
                        data=frames, file_path=FILE_PATH, file_name=file_name)
                    frames = []
                    self.data.put(file_name)
                    # print '%s: %s is producing %s to the queue!' %
                    # (time.ctime(), self.getName(), file_name)

                if start:
                    frames.append(buf)
                    count = count + 1
                    print "saving to file ..."
        stream.stop_stream()
        stream.close()
        pa.terminate()
        print "%s: %s finished!" % (time.ctime(), self.getName())


# Consumer thread
class Consumer(threading.Thread):

    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue
        self.recognition = BaiduVoice(configure='./config/config.ini')
        self.emit = Emit()

    def run(self):
        #print 'Consumer started'
        # print IS_EXIT
        while not IS_EXIT:
            # self.emit.emit_message(u'音乐',[u'音乐',u'备忘录'])
            #print 'consuming'
            try:
                file_name = self.data.get(True,3)
                print '%s: %s is consuming %s to the queue!' % (time.ctime(), self.getName(), file_name)
                message = self.recognition.get_text(
                    file_format='wav', audio_file=FILE_PATH + file_name)
                print message
                # print 'emitting'
                words = list(jieba.cut(message, cut_all=False))
                self.emit.emit_message(message, words)
                if IS_REMOVE:
                    os.remove(FILE_PATH + file_name)
            except Exception, e:
                pass
        print "%s: %s finished!" % (time.ctime(), self.getName())


def handler(signum, frame):
    global IS_EXIT
    IS_EXIT = True
    print "receive a signal %d, IS_EXIT = %d" % (signum, IS_EXIT)

      
def network():  
    fnull = open(os.devnull, 'w')
    result=subprocess.call('ping 114.114.114',shell=True,stdout=fnull,stderr=fnull)
    if result:
        return False
    else:
        return True
    fnull.close()

# Main thread
def main():
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    queue = Queue(10)
    producer = Producer('Pro.', queue)
    consumer = Consumer('Con.', queue)
    producer.setDaemon(True)
    consumer.setDaemon(True)
    producer.start()
    consumer.start()
    # producer.join()
    # consumer.join()
    while True:
        time.sleep(3)
        if not consumer.isAlive() and not producer.isAlive():
            break
    print 'All threads terminate!'

if __name__ == '__main__':
    main()
