from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

import alsaaudio

MODELDIR = "pocketsphinx/model"
DATADIR = "pocketsphinx/test/data"

# Create a decoder with certain model
# config = Decoder.default_config()
# config.set_string('-hmm', '../model/hmm/voxforge_en_sphinx.cd_cont_3000/')
# config.set_string('-lm', '../model/lm/voxforge_en_sphinx.cd_cont_3000/voxforge_en_sphinx.lm.DMP')
# config.set_string('-dict', '../model/lm/voxforge_en_sphinx.cd_cont_3000/voxforge_en_sphinx.dic')
# config.set_string('-logfn', '/dev/null')
# decoder=Decoder(config)


# # Decode streaming data.
# decoder=Decoder(config)
# decoder.start_utt()

# inp=alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, 'default')
# inp.setchannels(1)
# inp.setrate(16000)
# inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
# inp.setperiodsize(1024)

while True:
    try:
        length, data=inp.read()
        print length
        #if data:
            #decoder.process_raw(data, False, False)
        #print('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])
            #if 'yes' in [seg.word for seg in decoder.seg()]:
                #print 'OK'
        except Exception, e:
            pass
decoder.end_utt()
print('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])
