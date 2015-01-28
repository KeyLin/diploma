cd ~/Desktop
sudo apt-get install -y python2.7-dev
sudo apt-get install -y python-pip
sudo apt-get install -y speex
pip install pyrex --allow-all-external --allow-unverified pyrex
pip install pyaudio --allow-all-external --allow-unverified pyaudio
#ldconfig
echo "please install pySpeex"
wget http://downloads.xiph.org/releases/speex/speex-1.2rc2.tar.gz
tar -xzvf speex-1.2rc2.tar.gz
wget http://freenet.mcnabhosting.com/python/pySpeex/pySpeex-0.2.tar.gz
tar -xzvf pySpeex-0.2.tar.gz ./speex-1.2rc2/
python ./speex-1.2rc2/pySpeex/setup.py install
