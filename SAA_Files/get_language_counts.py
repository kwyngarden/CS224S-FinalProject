#!/usr/bin/env python
# Script to extract .mov filenames from a directory of html files
# of SAA speakers to a file where each line is the url to the
# corresponding SAA .mov file of that speaker. First argument
# should be the directory containing html files; second argument
# should be the output filename. Third argument gives the filename
# of a directory to which we write metadata about each speaker.

import re, os, sys

def extract_lang_counts(bio_filename, counts_filename):
	lang_counts = {}
	bio_file = open(bio_filename, 'r')
	lines = bio_file.readlines()
	for line in lines:
		tokens = line.split('\t')
		lang = tokens[2]
		if lang in lang_counts:
			lang_counts[lang] = lang_counts[lang] + 1
		else:
			lang_counts[lang] = 1

	bio_file.close()
	out_file = open(counts_filename, 'w')
	for lang in sorted(lang_counts, key=lang_counts.get, reverse=True):
		out_file.write(lang + "\t" + str(lang_counts[lang]) + "\n")
	out_file.close()


if __name__ == "__main__":
	extract_lang_counts(sys.argv[1], sys.argv[2])

