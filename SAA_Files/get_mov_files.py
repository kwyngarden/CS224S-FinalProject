#!/usr/bin/env python
# Script to download a list of .mov files from SAA and save them as
# wav files. First argument should be a file of line-separated pairs
# (tab-separated) of speaker ID and .mov file url. Second argument
# should be a directory to which we should write wav files.

import urllib, os, sys

def process_mov_files(mov_urls_file, output_dir):
	lines = open(mov_urls_file).readlines()
	for i in range(1451, len(lines)):
		line = lines[i]
		splitline = line.split()
		outfileName = output_dir + "/speaker" + splitline[0] + ".mov"
		urllib.urlretrieve(splitline[1], outfileName)

if __name__ == "__main__":
	process_mov_files(sys.argv[1], sys.argv[2])

	
