# -*- coding: utf-8 -*-
#!/bin/python

#from sphinx import Pocket
from baidu_voice import BaiduVoice
from save_file import SaveFile
from sender import Emit

from ctypes import *

import pyaudio
import time
from Queue import Queue
import threading
import signal
import os
import subprocess
import jieba
import alsaaudio
import ConfigParser

from pocketsphinx import *
from sphinxbase import *

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


CHUNK = 512
RATE = 16000
RECORD_SECONDS = 5
RECORD_CONTROL = int(RATE / CHUNK * RECORD_SECONDS)
FILE_PATH = './data/'
IS_REMOVE = False
IS_EXIT = False
WINDOW_SIZE = 30
card = 'default'


class Producer(threading.Thread):

    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.queue = queue

        config = ConfigParser.ConfigParser()
        config.read('./config/config.ini')

        # Create a config object for the Decoder, which will later decode our
        # spoken words.
        config_pocket = Decoder.default_config()
        config_pocket.set_string('-hmm', config.get('sphinx', 'hmm'))
        config_pocket.set_string('-lm', config.get('sphinx', 'lm'))
        config_pocket.set_string('-dict', config.get('sphinx', 'dic'))
        # Uncomment the following if you want to log only errors.
        config_pocket.set_string('-logfn', '/dev/null')

        self.decoder = Decoder(config_pocket)

        self.decoder.start_utt()


    def run(self):

        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
        inp.setchannels(1)
        inp.setrate(16000)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp.setperiodsize(CHUNK)

        #pocket = Pocket(configure='./config/config.ini')
        audio = SaveFile(SAMPLE_SIZE=2)
        start = False
        count = 0
        window = 0
        frames = []
        flag = False
        buf = []
        double = 2
        # print "Producer started"
        while not IS_EXIT:
            # print 'producing'
            #time.sleep(1)
            #print RECORD_CONTROL
            # print('Best hypothesis segments: ', [seg.word for seg in self.decoder.seg()])
            # if 'yes' in [seg.word for seg in self.decoder.seg()]:
            #     self.result = ['yes']
            #     print 'OK'
            #     self.decoder.end_utt()
            #self.decoder.start_utt()

            # Read the first Chunk from the microphone
            length,data = inp.read()
            #pocket.decode_buffer(audio_buf=data)
            if length%2 != 0:
                print length
            double -= 1
            buf.append(data)
            if double == 0:
                double = 2
                # print 'hehe'
                window += 1
                self.decoder.process_raw(b''.join(buf), False, False)
                print('Best hypothesis segments: ', [seg.word for seg in self.decoder.seg()])
                if 'yes' in [seg.word for seg in self.decoder.seg()]:
                    window = 0
                    flag = True
                    print 'OK'
                    self.decoder.end_utt()
                    self.decoder.start_utt()

                if window > WINDOW_SIZE:
                    window = 0
                    self.decoder.end_utt()
                    self.decoder.start_utt()

                if flag:
                    start = True
                    count = 0
                    # time.sleep(0.5)

                if count > RECORD_CONTROL:
                    start = False
                    count = 0
                    # time.sleep(0.5)
                    # pocket.set_flag()
                    file_name = SaveFile.set_name()
                    audio.save_wav(
                        data=frames, file_path=FILE_PATH, file_name=file_name)
                    frames = []
                    self.queue.put(file_name)
                    # print '%s: %s is producing %s to the queue!' %
                    # (time.ctime(), self.getName(), file_name)

                if start:
                    frames.append(b''.join(buf))
                    count = count + 1
                    print "saving to file ...",
                buf = []

        print "%s: %s finished!" % (time.ctime(), self.getName())


# Consumer thread
class Consumer(threading.Thread):

    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.queue = queue
        self.recognition = BaiduVoice(configure='./config/config.ini')
        self.emit = Emit()

    def run(self):
        # print 'Consumer started'
        # print IS_EXIT
        while not IS_EXIT:
            # self.emit.emit_message(u'音乐',[u'音乐',u'备忘录'])
            # print 'consuming'
            try:
                file_name = self.queue.get(True, 3)
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
    result = subprocess.call(
        'ping 114.114.114', shell=True, stdout=fnull, stderr=fnull)
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
