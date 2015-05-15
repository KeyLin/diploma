#!/bin/bash

arecord --channels=1 --rate=16000 --duration=3 --format=S16_LE --file-type raw ./data/cmd.pcm
