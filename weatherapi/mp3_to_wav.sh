#!/bin/bash

if [ ! -d converted/gao ]
then
 mkdir converted/gao;
fi;

for i in ./*.mp3
do
    sox "$i" "$(basename "$i" .mp3).wav"
done

for i in *.wav
 do sox -S "$i" -r 8k -b 16 -c 1 -e signed-integer "converted/gao/$i";
done
