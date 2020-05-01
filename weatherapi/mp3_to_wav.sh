#!/bin/bash

script_name=$1

if [ ! -d ./converted/$script_name ]
then
 mkdir ./converted/$script_name;
fi;

for i in ./*.mp3
do
    sox "$i" "$(basename "$i" .mp3).wav"
done

for i in ./*.wav
 do sox -S "$i" -r 8k -b 16 -c 1 -e signed-integer "converted/$script_name/$i";
done
