mkdir voice_recognition
cd voice_recognition
git clone git://github.com/cmusphinx/sphinxbase.git
cd sphinxbase
./autogen&&make&&make install
cd ..
git clone git://github.com/cmusphinx/pocketsphinx.git
cd pocketsphinx
./autogen&&make&&make install
cd ..
wget http://goofy.zamia.org/voxforge/de/voxforge-de-r20140813.tgz
tar xvzf voxforge-de-r20140813.tgz
cd voxforge-de-r20140813
nano run-pocketsphinx.sh