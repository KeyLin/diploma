set -e
myDir="~/Desktop/work-dir"
if [ ! -d "$myDir"]; then
	mkdir ~/Desktop/work-dir
fi

cd ~/Desktop/work-dir

dpkg -l | grep speex  > /dev/null
if [ $? -eq 0 ]; then
	echo "python2.7-dev already exit"
else
	apt-get install -y python2.7-dev
fi

dpkg -l | grep speex  > /dev/null
if [ $? -eq 0 ]; then
	echo "python-pip already exit"
else
	apt-get install -y python-pip
fi

dpkg -l | grep speex  > /dev/null
if [ $? -eq 0 ]; then
	echo "speex already exit"
else
	apt-get install -y speex
fi

pip freeze | grep Pyrex  > /dev/null
if [ $? -eq 0 ]; then
	echo "pyrex already exit"
else
	pip install pyrex
fi

pkg-config portaudio-2.0.pc  > /dev/null
if [ $? -eq 0 ]; then
    myFile0="./pa_stable_v19_20140130.tgz"
    if [ ! -f "$myFile0" ]; then
    	wget http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz
    fi
    tar -xzf pa_stable_v19_20140130.tgz -C
    ./portaudio/configure&&make clean&&make&&make install
fi

pip install pyaudio

echo "installing pySpeex"

myFile1="./speex-1.2rc2.tar.gz"
if [ ! -f "$myFile1" ]; then  
	wget http://downloads.xiph.org/releases/speex/speex-1.2rc2.tar.gz
	tar -xzf speex-1.2rc2.tar.gz  
fi

myFile2="./pySpeex-0.2.tar.gz"
if [ ! -f "$myFile2" ]; then  
	wget http://freenet.mcnabhosting.com/python/pySpeex/pySpeex-0.2.tar.gz
	tar -xzf pySpeex-0.2.tar.gz -C ./speex/
fi 

python ./speex*/pySpeex*/setup.py install
