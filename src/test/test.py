# -*- coding: utf-8 -*-
#!/usr/bin/env python 

# from baidu_voice import BaiduVoice
# import jieba

# test = BaiduVoice()

# print "pcm:",
# text1 = test.get_text(file_format = "pcm", audio_file = "./data/cmd.pcm")
# print text1
# seg_list = jieba.cut(text1, cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式

# print "wav:",
# text2 = test.get_text(file_format = "wav", audio_file = "./data/cmd.wav")
# print text2

import wave 
import struct 
import matplotlib.pyplot as plt 
 
data_set = [] 
f = wave.open('../data/cmd_01.wav', 'r') 
print '[+] WAV parameters ',f.getparams() 
print '[+] No. of Frames ',f.getnframes() 
for i in range(f.getnframes()): 
    single_frame = f.readframes(1)
    sint = struct.unpack('<h', single_frame)[0]
    data_set.append(sint) 
f.close() 
plt.plot(data_set) 
plt.ylabel('Amplitude')
plt.xlabel('Time') 
plt.show()

f = wave.open('../data/cmd_02.wav', 'r') 
print '[+] WAV parameters ',f.getparams() 
print '[+] No. of Frames ',f.getnframes() 
for i in range(f.getnframes()): 
    single_frame = f.readframes(1)
    sint = struct.unpack('<h', single_frame)[0]
    data_set.append(sint) 
f.close() 
plt.plot(data_set) 
plt.ylabel('Amplitude')
plt.xlabel('Time') 
plt.show()