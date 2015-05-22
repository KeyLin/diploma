import pyaudio

pa = pyaudio.PyAudio()

CHANNELS=1
RATE=16000
CHUNK=1024
FORMAT=pyaudio.paInt16

stream = pa.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=CHUNK)
print "*recording*"
frames = []

while True:
	data = stream.read(CHUNK)
    #frames.append(data)