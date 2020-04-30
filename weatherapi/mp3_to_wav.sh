#!/bin/bash 
for i in *.mp3
do
    sox "$i" "$(basename "$i" .mp3).wav"
done]
