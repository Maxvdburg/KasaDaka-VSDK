#!/bin/sh
script_name=$1
cd converted/$1
sox "forecast*" forecast.wav
sox "temp*" temperature.wav
sox "rain*" rain.wav
sox "wind*" wind.wav

find . -type f -name '*[0-9][0-9]*' -delete
