#!/bin/bash
str="'"
git add --all
echo $1
if [ "$1" = "" ]; then
	git commit -m ${str}$1${str}
else
	git commit -m 'default'
fi
git push
