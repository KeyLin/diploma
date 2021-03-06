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
package[3]=pkg-config
package[4]=portaudio19-dev
package[5]=python-pyaudio
package[6]=rabbitmq-server
package[7]=libportaudio2

#module[0]=PyAudio
module[0]=Pyrex
module[1]=requests
module[2]=jieba
module[3]=pika
module[4]=pyalsaudio
module[5]=RPi.GPIO

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

#rm -rf ../voiceRecognition
apt-get purge -y bluez-alsa

echo -e "\nSuccessfully deployed!\n"
