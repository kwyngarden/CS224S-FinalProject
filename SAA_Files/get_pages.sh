#!/bin/bash

for i in `seq 1 1960`;
do
	url="accent.gmu.edu/searchsaa.php?function=detail&speakerid="$i
	curl "$url" -o "html_files/speaker"$i".html"
done