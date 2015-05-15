# -*- coding: utf-8 -*-
#!/usr/bin/env python 

from Baidu import Baidu

# print "wav:",
# test0 = Baidu(file_format = "wav", audio_file = "data/cmd.spx.wav")
# test0.get_result()

print "pcm:",
test1 = Baidu(file_format = "pcm", audio_file = "../data/cmd.pcm")
test1.get_result()

print "baidu:",
test3 = Baidu(file_format = "speex", audio_file = "../data/baidu.spx")
test3.get_result()