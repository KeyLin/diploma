#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import pyaudio
import audioop
from ctypes import *
import subprocess
import ConfigParser
import sys
import time

from pocketsphinx import *
from sphinxbase import *

from save_file import SaveFile

#import locale
#locale.setlocale(locale.LC_ALL, '')    # set your locale

ERROR_HANDLER_FUNC = CFUNCTYPE(
    None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)


class Pocket(object):

    """docstring for Pocket"""

    def __init__(self, configure):
        super(Pocket, self).__init__()
        config = ConfigParser.ConfigParser()
        config.read(configure)

        # Create a config object for the Decoder, which will later decode our
        # spoken words.
        config_pocket = Decoder.default_config()
        config_pocket.set_string('-hmm', config.get('sphinx', 'hmm'))
        config_pocket.set_string('-lm', config.get('sphinx', 'lm'))
        config_pocket.set_string('-dict', config.get('sphinx', 'dic'))
        # Uncomment the following if you want to log only errors.
        config_pocket.set_string('-logfn', '/dev/null')

        # Create the decoder from the config
        self.decoder = Decoder(config_pocket)

        self.decoder.start_utt()
        # Needed to get the state, when you are speaking/not speaking ->
        # statusbar
        self.in_speech_bf = True

        self.result = ["hehe"]
        # print type(self.result)

    def get_flag(self, flag='yes'):
        if flag in self.result:
            return True
        else:
            return False

    def set_flag(self):
        self.result = ["hehe"]

    def decode_buffer(self, audio_buf):

        self.decoder.process_raw(audio_buf, False, False)
        try:
            # If the decoder has partial results, display them in the screen.
            if self.decoder.hyp().hypstr != '':
                result = self.decoder.hyp().hypstr
                #print('Partial decoding result: '+ result)
        except AttributeError:
            pass
        if self.decoder.get_in_speech():
            pass
        if self.decoder.get_in_speech() != self.in_speech_bf:
            self.in_speech_bf = self.decoder.get_in_speech()
            # When the speech ends:
            if not self.in_speech_bf:
                self.decoder.end_utt()
                try:
                    # Since the speech is ended, we can assume that we have
                    # final results, then display them
                    if self.decoder.hyp().hypstr != '':
                        self.result = self.decoder.hyp().hypstr.split(" ")
                        print(
                            'Stream decoding result:' + ",".join(self.result))

                except AttributeError:
                    pass
                # Say to the decoder, that a new "sentence" begins
                self.decoder.start_utt()

                print "Listening: No audio"

                #print("stopped listenning")
            else:
                print "Listening: Incoming audio..."
                pass


if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1,
                    rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()
    test = Pocket(configure='./config/config.ini')
    wav = SaveFile(sample_size=p.get_sample_size(pyaudio.paInt16))
    start = False
    frames = []
    while True:
        buf = stream.read(1024)  # Read the first Chunk from the microphone
        if buf:
            test.decode_buffer(audio_buf=buf)
            # print test.get_flag()
            if test.get_flag('yes'):
                start = True
                time.sleep(0.5)
                test.set_flag()

            if test.get_flag('no'):
                start = False
                time.sleep(0.5)
                test.set_flag()
                wav.save_wav(
                    data=frames, file_path='./data/', file_name=SaveFile.file_name('wav'))
                print "saved to wav file"
                wav.flush_frames()

            if start:
                frames.append(buf)
                print "saving to wav"

        else:
            break
