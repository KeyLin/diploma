from os import environ, path

MODELDIR = "../model/"
DATADIR = "./data"

from pocketsphinx import *
from sphinxbase import *
# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/'))
config.set_string('-lm', path.join(MODELDIR, 'lm/9633.lm'))
config.set_string('-dict', path.join(MODELDIR, 'lm/9633.dic'))
config.set_string('-logfn', '/dev/null')
# Decode streaming data.
decoder = Decoder(config)

print ("Pronunciation for word 'hello' is ", decoder.lookup_word("hello"))
print ("Pronunciation for word 'abcdf' is ", decoder.lookup_word("abcdf"))

decoder.start_utt()
stream = open(path.join(DATADIR, 'cmd.wav'), 'rb')
while True:
  buf = stream.read(1024)
  if buf:
    decoder.process_raw(buf, False, False)
  else:
    break
decoder.end_utt()

hypothesis = decoder.hyp()
print ('Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", hypothesis.prob)

print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])

# # Access N best decodings.
# print ('Best 10 hypothesis: ')
# for best, i in zip(decoder.nbest(), range(10)):
#     print (best.hypstr, best.score)