# -*- coding: utf-8 -*-
#!/bin/python

import wave
import sys
import time


class SaveFile(object):

    """docstring for SaveFile"""

    def __init__(self, sample_size, CHANNELS=1, RATE=16000, CHUNK=1024):
        super(SaveFile, self).__init__()
        self.sample_size = sample_size
        self.channels = CHANNELS
        self.rate = RATE
        self.chunk = CHUNK

    def save_wav(self, data, file_path, file_name):
        wf = wave.open(file_path + file_name, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sample_size)

        wf.setframerate(self.rate)
        wf.writeframes(b''.join(data))

        wf.close()

    @staticmethod
    def set_name(suffix=''):
        return time.strftime('%Y%m%d%H%M%S') + suffix


if __name__ == "__main__":
    print SaveFile.file_name('wav')
    pass
