#!/usr/bin/env python

## recordtest.py
##
## This is an example of a simple sound capture script.
##
## The script opens an ALSA pcm forsound capture. Set
## various attributes of the capture, and reads in a loop,
## writing the data to standard out.
##
## To test it out do the following:
## python recordtest.py out.raw # talk to the microphone
## aplay -r 8000 -f S16_LE -c 1 out.raw

#!/usr/bin/env python

from __future__ import print_function

import sys
import time
import getopt
import alsaaudio
import ConfigParser
from pocketsphinx import *
from sphinxbase import *


def usage():
    print('usage: recordtest.py [-c <card>] <file>', file=sys.stderr)
    sys.exit(2)

if __name__ == '__main__':

    card = 'default'

    opts, args = getopt.getopt(sys.argv[1:], 'c:')
    for o, a in opts:
        if o == '-c':
            card = a

    if not args:
        usage()

    f = open(args[0], 'wb')

    # Open the device in nonblocking capture mode. The last argument could
    # just as well have been zero for blocking mode. Then we could have
    # left out the sleep call in the bottom of the loop
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)

    # Set attributes: Mono, 44100 Hz, 16 bit little endian samples
    inp.setchannels(1)
    inp.setrate(16000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

    # The period size controls the internal number of frames per period.
    # The significance of this parameter is documented in the ALSA api.
    # For our purposes, it is suficcient to know that reads from the device
    # will return this many frames. Each frame being 2 bytes long.
    # This means that the reads below will return either 320 bytes of data
    # or 0 bytes of data. The latter is possible because we are in nonblocking
    # mode.
    inp.setperiodsize(160)

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

    decoder = Decoder(config_pocket)

    decoder.start_utt()
    
    loops = 1000000
    while True:
        #loops -= 1
        # Read data from device
        l, data = inp.read()
        print(l)
        if l:
            #decoder.process_raw(data, False, False)
            #print('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])
            time.sleep(.001)
        if l < 0 :
            print('errors')
            break