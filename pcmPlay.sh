#!/bin/bash

aplay -t raw -c 1 -f S16_LE -r 16000 $1
