#!/bin/sh
script_name=$1
cd converted/$1
sox "en_*" en_weatherforecast.wav
sox "fr_*" fr_weatherforecast.wav

find . -type f -name '*[0-9][0-9]*' -delete
