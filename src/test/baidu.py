#-*- coding: utf-8 -*-
#!/usr/bin/env python 
import sys
sys.path.append("../")
from baidu_voice import BaiduVoice
import jieba

test = BaiduVoice(configure='../config/config.ini')

text = test.get_text(file_format = "wav", audio_file = "../data/cmd.wav")
print text
seg_list = jieba.cut(text)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

# text = test.get_text(file_format = "wav", audio_file = "../data/out.wav")
# print text
# seg_list = jieba.cut(text, cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式

# text = test.get_text(file_format = "wav", audio_file = "../data/cmd_03.wav")
# print text
# seg_list = jieba.cut(text, cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式

# text = test.get_text(file_format = "wav", audio_file = "../data/cmd_04.wav")
# print text
# seg_list = jieba.cut(text, cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式

# text = test.get_text(file_format = "wav", audio_file = "../data/cmd_05.wav")
# print text
# seg_list = jieba.cut(text, cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式