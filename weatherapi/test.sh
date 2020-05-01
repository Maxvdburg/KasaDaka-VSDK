#!/bin/sh
script_name=$1
cd converted/$1
for x in ./*
do
        if [ "$x" != "forecast.wav, sun.wav, wind.wav, temperature.wav" ]
        then
                rm -f $x;
        fi
done;
