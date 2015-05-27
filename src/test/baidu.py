#-*- coding: utf-8 -*-
#!/usr/bin/env python 
import sys
sys.path.append("../")
from baidu_voice import BaiduVoice
import jieba

jieba.initialize()

test = BaiduVoice(configure='../config/config.ini')

# result[1] = test.get_result(file_format = "wav", audio_file = "../data/rasp.wav")
# print result[1]
# seg_list = jieba.cut(result[1])
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式

result = test.get_result(file_format = "wav", audio_file = "../data/cmd.wav")
print 'Recognition'+result[1]
seg_list = jieba.cut(result[1])
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

result = test.get_result(file_format = "wav", audio_file = "../data/cmd_01.wav")
print 'Recognition'+result[1]
seg_list = jieba.cut(result[1])
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

result = test.get_result(file_format = "wav", audio_file = "../data/cmd_02.wav")
print 'Recognition'+result[1]
seg_list = jieba.cut(result[1])
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

result = test.get_result(file_format = "wav", audio_file = "../data/cmd_03.wav")
print 'Recognition'+result[1]
seg_list = jieba.cut(result[1])
print("Full Mode: " + "/ ".join(seg_list))  # 全模式