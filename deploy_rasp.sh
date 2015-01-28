set -e
cd ~/Desktop
apt-get install -y python2.7-dev
apt-get install -y python-pip
apt-get install -y speex
pip install pyrex --allow-all-external --allow-unverified pyrex
pip install pyaudio --allow-all-external --allow-unverified pyaudio
#ldconfig
echo "installing pySpeex"

myFile1="./speex-1.2rc2.tar.gz"
myFile2="./pySpeex-0.2.tar.gz"

if [ ! -f "$myFile1"]; then  
wget http://downloads.xiph.org/releases/speex/speex-1.2rc2.tar.gz  
fi
if [ ! -f "$myFile2"]; then  
wget http://freenet.mcnabhosting.com/python/pySpeex/pySpeex-0.2.tar.gz  
fi  
tar -xzvf speex-1.2rc2.tar.gz
tar -xzvf pySpeex-0.2.tar.gz -C ./speex-1.2rc2/
python ./speex*/pySpeex*/setup.py install
