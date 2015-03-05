#!/bin/bash

git add --all
echo $1
if [ "$1" = "" ]; then
	git commit -m 'default'
else
	str="$1"
	git commit -m "$str"
fi
git push
