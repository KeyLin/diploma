#!/bin/bash

myDir="sphinx_install"
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
        echo "Package:$1 already exist"
    else
        apt-get install -y $1 || { echo "Package:$1 install failed"; exit 1; } 
        echo "Package:$1 successfully installed"
    fi
    return 0;
}

function ModuleInstall()
{
    pip freeze | grep $1  > /dev/null
    if [ $? -eq 0 ]; then
        echo "Module:$1 already exist"
    else
        pip install $1  --allow-external $1 --allow-unverified $1 || { echo "Module:$1 install failed"; exit 1; }
        echo "Module:$1 successfully installed"
    fi
}

for ((i=0;i<${#package[@]};i++));
    do
        #echo ${package[i]}
        PackageInstall ${package[i]}
    done 

pkg-config --list-all | grep sphinxbase > /dev/null
if [ $? -eq 1 ]; then
    myFile0="./sphinxbase-5prealpha.tar.gz"
    myDir0="./sphinxbase-5prealpha"
    if [ ! -f "$myFile0" ]; then
        wget http://softlayer-sng.dl.sourceforge.net/project/cmusphinx/sphinxbase/5prealpha/sphinxbase-5prealpha.tar.gz
    fi
    if [ ! -d "$myDir0" ]; then
        tar -xzvf sphinxbase-5prealpha.tar.gz
    fi
    ./sphinxbase-5prealpha/configure && make &&sudo make install || { echo "sphinxbase install failed"; exit 1; }
    echo "sphinxbase successfully installed"
else echo "sphinxbase already exist "
fi

pkg-config --list-all | grep pocketsphinx > /dev/null
if [ $? -eq 1 ]; then
    myFile0="./pocketsphinx-5prealpha.tar.gz"
    myDir0="./pocketsphinx-5prealpha"
    if [ ! -f "$myFile0" ]; then
        wget http://softlayer-sng.dl.sourceforge.net/project/cmusphinx/pocketsphinx/5prealpha/pocketsphinx-5prealpha.tar.gz
    fi
    if [ ! -d "$myDir0" ]; then
        tar -xzvf pocketsphinx-5prealpha.tar.gz
    fi
    ./pocketsphinx-5prealpha/configure && sudo make install || { echo "pocketsphinx install failed"; exit 1; }
    echo export LD_LIBRARY_PATH=/usr/local/lib | sudo tee -a /etc/profile 
    echo export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig | sudo tee -a /etc/profile
    source /etc/profile  
    echo "pocketsphinx successfully installed"
else echo "pocketsphinx already exist "
fi

sphinxDir="/usr/sphinx-tools/"
#安装声学模型训练工具
if [ ! -d "${sphinxDir}/sphinxtrain" ]; then
    myFile0="./sphinxtrain-5prealpha.tar.gz"
    myDir0="./sphinxtrain-5prealpha"
    if [ ! -f "$myFile0" ]; then
        wget http://softlayer-sng.dl.sourceforge.net/project/cmusphinx/sphinxtrain/5prealpha/sphinxtrain-5prealpha.tar.gz
    fi
    if [ ! -d "$myDir0" ]; then
        tar -xzvf sphinxtrain-5prealpha.tar.gz
    fi
    sudo bash sphinxtrain-5prealpha/configure --prefix=${sphinxDir}/sphinxtrain && sudo make && sudo make install || { echo "sphinxtrain install failed"; exit 1; }
    echo "sphinxtrain successfully installed"
else echo "sphinxtrain already exist "
fi
#安装语言模型训练工具
if [ ! -d "${sphinxDir}/cmuclmtk" ]; then
    myFile0="./cmuclmtk-0.7.tar.gz"
    myDir0="./cmuclmtk-0.7"
    if [ ! -f "$myFile0" ]; then
        wget http://nchc.dl.sourceforge.net/project/cmusphinx/cmuclmtk/0.7/cmuclmtk-0.7.tar.gz
    fi
    if [ ! -d "$myDir0" ]; then
        tar -xzvf cmuclmtk-0.7.tar.gz
    fi
    sudo bash cmuclmtk-0.7/configure --prefix=${sphinxDir}/cmuclmtk && sudo make && sudo make install|| { echo "cmuclmtk-0.7 install failed"; exit 1; }
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