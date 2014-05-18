#!/bin/bash

for i in `seq 1 1956`;
do
	ffmpeg -i "mov_files/speaker"$i".mov" -vn "wav_files/speaker"$i".wav"
done
