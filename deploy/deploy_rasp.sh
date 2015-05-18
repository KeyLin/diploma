#!/bin/bash
#set -e

myDir="/tmp/voiceRecognition"
if [ ! -d "$myDir" ]; then
	mkdir "$myDir"
fi

cd "$myDir"

declare -a package
declare -a module

package[0]=libogg-dev
package[1]=python2.7-dev
package[2]=python-pip
package[3]=speex
package[4]=libspeex-dev
package[5]=pkg-config
package[6]=libportaudio2
package[7]=portaudio19-dev
package[8]=python-pyaudio
package[9]=rabbitmq-server

#module[0]=PyAudio
module[0]=Pyrex
module[1]=requests


function PackageInstall()
{
	#echo $1
	dpkg -l | grep $1  > /dev/null
	if [ $? -eq 0 ]; then
		echo "$1 already exist"
	else
		apt-get install -y $1 || { echo "$1 install failed"; exit 1; } 
		echo "$1 successfully installed"
	fi
	return 0;
}

function ModuleInstall()
{
	pip freeze | grep $1  > /dev/null
	if [ $? -eq 0 ]; then
		echo "$1 already exist"
	else
		pip install $1  --allow-external $1 --allow-unverified $1 || { echo "$1 install failed"; exit 1; }
		echo "$1 successfully installed"
	fi
}

for ((i=0;i<${#package[@]};i++));
	do
		#echo ${package[i]}
		PackageInstall ${package[i]}
	done 

for ((i=0;i<${#module[@]};i++));
	do
		#echo ${package[i]}
		ModuleInstall ${module[i]}
	done

#notice:jack* may cause audio record problem.Just remove jack*.

#myFile1="./speex-1.2rc1.tar.gz"
#if [ ! -f "$myFile1" ]; then  
#	wget http://downloads.xiph.org/releases/speex/speex-1.2rc1.tar.gz
#	tar -xzvf speex-1.2rc1.tar.gz  
#fi

#rm -rf ../voiceRecognition
apt-get purge -y bluez-alsa

echo -e "\nSuccessfully deployed!\n"
