#!/bin/sh
script_name=$1
cd converted/$1
sox "forecast*" forecast.wav
sox "maximum_temp*" temperature.wav
sox "sun*" sun.wav
sox "wind*" wind.wav
