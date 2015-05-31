#!/usr/bin/env python
#coding:utf8

import math
import numpy as np
import wave

class VAD(object):
    """docstring for VAD"""
    def __init__(self, frame_size = 256, over_lap = 128):
        super(VAD, self).__init__()
        self.frame_size = frame_size
        self.over_lap = over_lap
        
    # method 1: absSum
    def get_volume(self,wave_data):
        wave_data = np.fromstring(wave_data, dtype=np.int16)
        wave_data = wave_data*1.0/max(abs(wave_data))  # normalization
        wlen = len(wave_data)
        step = self.frame_size - self.over_lap
        frame_num = int(math.ceil(wlen*1.0/step))
        volume = np.zeros(frame_num)
        for i in range(frame_num):
            cur_frame = wave_data[np.arange(i*step,min(i*step+self.frame_size,wlen))]
            cur_frame = cur_frame - np.median(cur_frame) # zero-justified
            volume[i] = np.sum(np.abs(cur_frame))
        return volume

    # method 2: 10 times log10 of square sum
    def get_volumeDB(self,wave_data):
        wave_data = np.fromstring(wave_data, dtype=np.int16)
        wave_data = wave_data*1.0/max(abs(wave_data))  # normalization
        wlen = len(wave_data)
        step = self.frame_size - self.over_lap
        frame_num = int(math.ceil(wlen*1.0/step))
        volume = np.zeros(frame_num)
        for i in range(frame_num):
            cur_frame = wave_data[np.arange(i*step,min(i*step+self.frame_size,wlen))]
            cur_frame = cur_frame - np.mean(cur_frame) # zero-justified
            volume[i] = 10*np.log10(np.sum(cur_frame*cur_frame))
        return volume

    @staticmethod
    def string_split(string,width):
        return [string[x:x+width] for x in range(0,len(string),width)]

    def remove_mute(self,input_file,output_file,case = 1):
        wf = wave.open(input_file,'r')
        params = wf.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        wave_data = wf.readframes(nframes)
        wf.close()

        volume = self.get_volume(wave_data)

        if case == 1:
            threshhold = max(volume)*0.10
        if case == 2:
            threshhold = min(volume)*10.0
        if case == 3: 
            threshhold = max(volume)*0.05+min(volume)*5.0

        wave_data = self.string_split(wave_data,self.frame_size)
        length = len(wave_data)

        # print len(volume)
        # print len(wave_data)

        frames = []
        start = 0
        end = length-1
        for i in range(len(volume)):
            if(volume[i]-threshhold)>0:
                start = i
                break
        while(end > start):
            if (volume[end]-threshhold)<0:
                break
            else:
                end = end - 1

        print start
        print end

        for i in xrange(start,end):
            frames.append(wave_data[i])

        wf = wave.open(output_file,"wb")
        wf.setnchannels(nchannels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)
        wf.writeframes(b''.join(frames))

if __name__ == '__main__':
    test = VAD()
    test.remove_mute(input_file = './data/cmd.wav',output_file = './data/new.wav',case = 2)
