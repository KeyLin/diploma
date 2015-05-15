#!/bin/bash

myDir="/home/killin/sphinx_install"
if [ ! -d "$myDir" ]; then
	mkdir "$myDir"
fi

cd "$myDir"

declare -a package
declare -a module

package[0]=bison
package[1]=swig
# package[2]=sphinxbase-utils

# package[3]=libpocketsphinx-dev
# package[4]=libpocketsphinx1

# package[5]=python-sphinxbase
# package[6]=python-pocketsphinx
# python-pocketsphinx-dbg 

# package[7]=pocketsphinx-lm-zh-hans-gigatdt 
module[0]=pocketsphinx

function PackageInstall()
{
	#echo $1
	dpkg -l | grep $1  > /dev/null
	if [ $? -eq 0 ]; then
		echo "package: $1 already exist"
	else
		sudo apt-get install -y $1 || { echo "package: $1 install failed"; exit 1; } 
		echo "package: $1 successfully installed"
	fi
	return 0;
}

function ModuleInstall()
{
	pip freeze | grep $1  > /dev/null
	if [ $? -eq 0 ]; then
		echo "python module: $1 already exist"
	else
		sudo pip install $1  --allow-external $1 --allow-unverified $1 || { echo "python module: $1 install failed"; exit 1; }
		echo "python module: $1 successfully installed"
	fi
}

for ((i=0;i<${#package[@]};i++));
	do
		#echo ${package[i]}
		PackageInstall ${package[i]}
	done 

pkg-config --list-all | grep sphinxbase > /dev/null
if [ $? -eq 0 ]; then
    myFile0="./sphinxbase-0.8.tar.gz"
    myDir0="./sphinxbase-0.8"
    if [ ! -f "$myFile0" ]; then
    	wget http://nchc.dl.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz
    fi
    if [ ! -d "$myDir0" ]; then
    	tar -xzvf sphinxbase-0.8.tar.gz
    fi
    ./sphinxbase-0.8/configure && make && sudo make install || { echo "sphinxbase install failed"; exit 1; }
    echo export LD_LIBRARY_PATH=/usr/local/lib | sudo tee -a /etc/profile 
    echo export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig | sudo tee -a /etc/profile
    source /etc/profile 
    echo "sphinxbase successfully installed"
else echo "sphinxbase already exist "
fi

pkg-config --list-all | grep pocketsphinx > /dev/null
if [ $? -eq 0 ]; then
    myFile0="./pocketsphinx-0.8.tar.gz"
    myDir0="./pocketsphinx-0.8"
    if [ ! -f "$myFile0" ]; then
    	wget http://nchc.dl.sourceforge.net/project/cmusphinx/pocketsphinx/0.8/pocketsphinx-0.8.tar.gz
    fi
    if [ ! -d "$myDir0" ]; then
    	tar -xzvf pocketsphinx-0.8.tar.gz
    fi
    ./pocketsphinx-0.8/configure && sudo make install || { echo "pocketsphinx install failed"; exit 1; } 
    echo "pocketsphinx successfully installed"
else echo "pocketsphinx already exist "
fi

sphinxToolsDir="/usr/sphinx-tools-1.08/"

#安装声学模型训练工具
if [ ! -d "${sphinxToolsDir}/sphinxtrain" ]; then
    myFile0="./sphinxtrain-1.0.8.tar.gz"
    myDir0="./sphinxtrain-1.0.8"
    if [ ! -f "$myFile0" ]; then
        wget http://nchc.dl.sourceforge.net/project/cmusphinx/sphinxtrain/1.0.8/sphinxtrain-1.0.8.tar.gz
    fi
    if [ ! -d "$myDir0" ]; then
        tar -xzvf sphinxtrain-1.0.8.tar.gz
    fi
    ./sphinxtrain-1.0.8/configure --prefix=${sphinxToolsDir}/sphinxtrain && sudo make &&sudo make install || { echo "sphinxtrain install failed"; exit 1; }
    echo "sphinxtrain successfully installed"
else echo "sphinxtrain already exist "
fi

#安装语言模型训练工具
if [ ! -d "${sphinxToolsDir}/cmuclmtk" ]; then
    myFile0="./cmuclmtk-0.7.tar.gz"
    myDir0="./cmuclmtk-0.7"
    if [ ! -f "$myFile0" ]; then
    	wget http://nchc.dl.sourceforge.net/project/cmusphinx/cmuclmtk/0.7/cmuclmtk-0.7.tar.gz
    fi
    if [ ! -d "$myDir0" ]; then
    	tar -xzvf cmuclmtk-0.7.tar.gz
    fi
    ./cmuclmtk-0.7/configure --prefix=${sphinxToolsDir}/cmuclmtk && make && sudo make install || { echo "cmuclmtk-0.7 install failed"; exit 1; }
    echo "cmuclmtk-0.7 successfully installed"
else echo "cmuclmtk-0.7 already exist "
fi

for ((i=0;i<${#module[@]};i++));
	do
		#echo ${package[i]}
		ModuleInstall ${module[i]}
	done 

#pocketsphinx_continuous -samprate 16000/8000/48000 
#rm -rf ../voiceRecognition
echo -e "\nSuccessfully deployed!\n"
