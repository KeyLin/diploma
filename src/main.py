# -*- coding: utf-8 -*-
#!/bin/python

from sphinx import Pocket
from baidu_voice import BaiduVoice
from save_file import SaveFile
from sender import Emit
import status

from ctypes import *

import pyaudio
import time
from Queue import Queue
import threading
import signal
import os
import subprocess
import jieba
import urllib2

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# import locale
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
IS_TEST = False

class Producer(threading.Thread):

    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        global event
        if not IS_TEST:
            pa = pyaudio.PyAudio()
            stream = pa.open(format=pyaudio.paInt16, channels=1,
                             rate=RATE, input=True, frames_per_buffer=CHUNK)
            stream.start_stream()
        else:
            wf = wave.open('./data/test.wav', 'rb')

        pocket = Pocket(configure='./config/config.ini')
        audio = SaveFile(SAMPLE_SIZE=pa.get_sample_size(pyaudio.paInt16))
        start = False
        count = 0
        frames = []
        # print "Producer started"
        status.set_color(color='blue')
        while not IS_EXIT:
            if not IS_TEST:
                buf = stream.read(CHUNK)
            else:
                buf = wf.readframes(CHUNK)

            if buf and event.isSet():
                if not start:
                    status.set_color(color='green')
                    pocket.decode_buffer(audio_buf=buf)

                if pocket.get_flag(flag='HEY'):
                    status.set_color(color='blue')
                    start = True
                    count = 0
                    # time.sleep(0.5)
                    pocket.set_flag()

                if count > RECORD_CONTROL:
                    status.set_color(color='green')
                    start = False
                    count = 0
                    # time.sleep(0.5)
                    pocket.set_flag()
                    file_name = SaveFile.set_name()
                    audio.save_wav(
                        data=frames, file_path=FILE_PATH, file_name=file_name)
                    frames = []
                    self.data.put(file_name)

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
        # print 'Consumer started'
        global event
        # print IS_EXIT
        while not IS_EXIT:
            # print 'consuming'
            event.wait()
            try:
                file_name = self.data.get(True, 3)
                print '%s: %s is consuming %s to the queue!' % (time.ctime(), self.getName(), file_name)
                message = self.recognition.get_result(
                    file_format='wav', audio_file=FILE_PATH + file_name)
                # print message
                # print 'emitting'
                if(message[0] == 0):
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


def internet():
    try:
        response = urllib2.urlopen('https://www.baidu.com/', timeout=0.1)
        return True
    except urllib2.URLError as err:
        pass
    return False

# Main thread

event = threading.Event()
event.clear()


def main():
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    queue = Queue(10)
    producer = Producer('Listening.', queue)
    consumer = Consumer('Sending.', queue)
    producer.setDaemon(True)
    consumer.setDaemon(True)
    producer.start()
    consumer.start()
    # producer.join()
    # consumer.join()
    while True:
        time.sleep(0.5)
        if IS_EXIT:
            event.set()
        if not consumer.isAlive() and not producer.isAlive():
            break
        if internet():
            event.set()
        else:
            print "No internet access"
            status.set_color(color='red')
            print "Red warning"
            event.clear()

    print 'All threads terminate!'
    status.reset()


if __name__ == '__main__':
    jieba.initialize()
    main()
