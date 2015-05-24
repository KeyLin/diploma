import wave
import numpy as np
import matplotlib.pyplot as plt
import volume as vp
import re

def findIndex1(vol,thres):
    length = len(vol)
    print length
    index = [0]
    for i in range(length-1):
        if((vol[i]-thres)*(vol[i+1]-thres)<0):
            index.append(i)
    index = np.array(index)
    return index

def findIndex2(vol,thres):
    length = len(vol)
    print length
    index = [0]
    for i in range(length-1):
        if((vol[i]-thres)*(vol[i+1]-thres)<0):
            index.append(i)
    index.append(length-1)

    print len(index)
    print index
    i = 0
    while (i < len(index)-2):
        if (index[i+1]-index[i])<125 and (index[i+2]-index[i+1])<125:
            del index[i+1]
            continue
        i = i+1

    print index
    index = np.array(index)
    return index

fw = wave.open('../data/cmd.wav','r')
params = fw.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
strData = fw.readframes(nframes)
waveData1 = np.fromstring(strData, dtype=np.int16)
waveData = waveData1*1.0/max(abs(waveData1))  # normalization
fw.close()

frameSize = 256
overLap = 128
vol = vp.calVolume(waveData,frameSize,overLap)
threshold1 = max(vol)*0.14
threshold2 = min(vol)*10.0
threshold3 = max(vol)*0.01+min(vol)*5.0

time = np.arange(0,nframes) * (1.0/framerate)
frame = np.arange(0,len(vol)) * (nframes*1.0/len(vol)/framerate)
index1 = findIndex1(vol,threshold1)*(nframes*1.0/len(vol)/framerate)
index2 = findIndex1(vol,threshold2)*(nframes*1.0/len(vol)/framerate)
index3 = findIndex1(vol,threshold3)*(nframes*1.0/len(vol)/framerate)
end = nframes * (1.0/framerate)
print nframes

def sp(string,width):
    return [string[x:x+width] for x in range(0,len(string),width)]

#strData1=re.findall(r'.{len(vol)}',strData)
strData1 = sp(strData,256)

#print strData1
length = len(waveData1)
print len(vol)
print len(strData1)
frames = []
start = 100
# for i in range(len(vol)):
#     if(vol[i]-threshold1)>0:
#         start = i
#         break
print start
while(start < len(vol)-50):
    frames.append(strData1[start])
    start=start+1
wf = wave.open('../data/new.wav',"wb")
wf.setnchannels(nchannels)
wf.setsampwidth(sampwidth)
wf.setframerate(framerate)
wf.writeframes(b''.join(frames))


plt.subplot(211)
plt.plot(time,waveData,color="black")
plt.plot([index1,index1],[-2,2],'-r')
plt.plot([index2,index2],[-2,2],'-g')
plt.plot([index3,index3],[-2,2],'-b')
plt.ylabel('Amplitude')

plt.subplot(212)
plt.plot(frame,vol,color="black")
plt.plot([0,end],[threshold1,threshold1],'-r', label="threshold 1:"+str(threshold1))
plt.plot([0,end],[threshold2,threshold2],'-g', label="threshold 2:"+str(threshold2))
plt.plot([0,end],[threshold3,threshold3],'-b', label="threshold 3:"+str(threshold3))
plt.legend()
plt.ylabel('Volume(absSum)')
plt.xlabel('time(seconds)')
plt.show()