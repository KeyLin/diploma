# -*- coding: utf-8 -*-
#!/bin/python

import pyaudio
import wave
import sys

from ctypes import *
from contextlib import contextmanager

ERROR_HANDLER_FUNC = CFUNCTYPE(
    None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)


class RecordAndPlay(object):

    """docstring for RecordAndPlay"""

    def __init__(self):
        super(RecordAndPlay, self).__init__()

    def record_wav(self, WAVE_OUTPUT_FILENAME, RECORD_SECONDS=5, CHANNELS=1, RATE=16000, CHUNK=1024, FORMAT=pyaudio.paInt16):
        pa = pyaudio.PyAudio()
        stream = pa.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         input=True,
                         frames_per_buffer=CHUNK)
        print "*recording*"
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print "*done recording*"

        stream.stop_stream()
        stream.close()
        pa.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pa.get_sample_size(FORMAT))

        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

        wf.close()

    def play_wav(self, audio_file, chunk=1024):
        wf = wave.open(audio_file, 'rb')

        pa = pyaudio.PyAudio()

        stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
                         channels=wf.getnchannels(),
                         rate=wf.getframerate(),
                         output=True)

        data = wf.readframes(chunk)

        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()

        pa.terminate()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Record a wave file.\n\nUsage: %s -r filename.wav -t time" %
              sys.argv[0])
        print("Plays a wave file.\n\nUsage: %s -p filename.wav" % sys.argv[0])
        sys.exit(-1)
    test = RecordAndPlay()
    if sys.argv[1] == '-r':
        test.record_wav(
            WAVE_OUTPUT_FILENAME=sys.argv[2], RECORD_SECONDS=int(sys.argv[4]))
    if sys.argv[1] == '-p':
        test.play_wav(audio_file=sys.argv[2])
