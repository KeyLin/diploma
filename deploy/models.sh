#!/bin/bash

myDir="../sphinx/cmu"
if [ ! -d "$myDir" ]; then
	mkdir "$myDir"
fi

cd "$myDir"

wget http://nchc.dl.sourceforge.net/project/cmusphinx/Acoustic%20and%20Language%20Models/Mandarin%20Language%20Model/zh_broadcastnews_64000_utf8.DMP

wget http://nchc.dl.sourceforge.net/project/cmusphinx/Acoustic%20and%20Language%20Models/Mandarin%20Language%20Model/zh_broadcastnews_utf8.dic

wget http://nchc.dl.sourceforge.net/project/cmusphinx/Acoustic%20and%20Language%20Models/Mandarin%20Broadcast%20News%20acoustic%20models/zh_broadcastnews_16k_ptm256_8000.tar.bz2
bzip2 -d zh_broadcastnews_16k_ptm256_8000.tar.bz2
tar -b -xzvf zh_broadcastnews_16k_ptm256_8000.tar.bz2
