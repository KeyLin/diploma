set -e
cd ~/Desktop
apt-get install -y python2.7-dev
apt-get install -y python-pip
apt-get install -y speex
pip install pyrex

myFile0="./pa_stable_v19_20140130.tgz"
if [ ! -f "$myFile0" ]; then
wget http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz
fi
tar -xzf pa_stable_v19_20140130.tgz portaudio
{./portaudio/configure&&make clean&&make&&make install}||{ echo "portaudio install error"; exit 1; }

pip install pyaudio

echo "installing pySpeex"

myFile1="./speex-1.2rc2.tar.gz"
if [ ! -f "$myFile1" ]; then  
wget http://downloads.xiph.org/releases/speex/speex-1.2rc2.tar.gz  
fi

myFile2="./pySpeex-0.2.tar.gz"
if [ ! -f "$myFile2" ]; then  
wget http://freenet.mcnabhosting.com/python/pySpeex/pySpeex-0.2.tar.gz  
fi  
tar -xzf speex-1.2rc2.tar.gz speex
tar -xzf pySpeex-0.2.tar.gz pySpeex -C ./speex/
python ./speex/pySpeex/setup.py install
