#!/bin/sh
script_name=$1
cd converted/$1
sox "en_forecast*" en_forecast.wav
sox "en_temp*" en_temperature.wav
sox "en_rain*" en_rain.wav
sox "en_wind*" en_wind.wav

sox "fr_forecast*" fr_forecast.wav
sox "fr_temp*" fr_temperature.wav
sox "fr_rain*" fr_rain.wav
sox "fr_wind*" fr_wind.wav

find . -type f -name '*[0-9][0-9]*' -delete
