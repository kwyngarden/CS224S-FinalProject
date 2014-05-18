#!/usr/bin/env python
# Script to extract .mov filenames from a directory of html files
# of SAA speakers to a file where each line is the url to the
# corresponding SAA .mov file of that speaker. First argument
# should be the directory containing html files; second argument
# should be the output filename. Third argument gives the filename
# of a directory to which we write metadata about each speaker.

import re, os, sys

def get_mov_file(pattern, fileContents):
	match = pattern.search(fileContents)
	if not match:
		return None
	return match.group()[5:-1]

def save_bio_data(idNum, data, outfile):
	try:
		elems = re.findall('<li>.*?</li>', data, re.DOTALL)
		birth_place = re.search('</em>.*<a', elems[0]).group()[6:-3]
		native_lang = re.search('">.*</a>', elems[1]).group()[2:-4]
		other_langs = re.search('</em>.*</li>', elems[2]).group()[5:-5]
		age = re.search('</em> .*,', elems[3]).group()[6:-1]
		sex = re.search('((male)|(female))', elems[3]).group()
		age_english_onset = re.search('</em> .*</li>', elems[4]).group()[6:-5]
		english_learn_method = re.search('</em> .*</li>', elems[5]).group()[6:-5]
		english_residence = re.search('</em> .*</li>', elems[6]).group()[6:-5]
		len_english_residence = re.search('</em> .* </li>', elems[7]).group()[6:-6]
		line = (birth_place+'\t'+native_lang+'\t'+other_langs+'\t'+age+'\t'+sex+'\t'
				''+age_english_onset+'\t'+english_learn_method+'\t'+english_residence+'\t'
				''+len_english_residence)
		outfile.write(str(idNum) + '\t' + line + '\n')
		return
	except AttributeError:
		return

def extract_mov_files(inputDirName, outputName, metadataOut):
	outfile = open(outputName, 'w')
	metafile = open(metadataOut, 'w')
	pattern = re.compile('src=".*\.mov"')

	for filename in os.listdir(inputDirName):
		filename = inputDirName+filename
		if os.path.isfile(filename):
			idNum = int(re.search('\d+', filename).group())
			inFile = open(filename, 'r')
			contents = inFile.read()
			#print "Read {} with id {} into:\n\n".format(filename, idNum)
			mov_file = get_mov_file(pattern, contents)
			
			if mov_file is not None:
				outfile.write(str(idNum) + '\t' + mov_file + '\n')
		
		
			metadataSection = re.search('<ul class="bio">.*?</ul>', contents, re.DOTALL)
			if metadataSection is not None:
				#print "Got data:\n\n"+metadataSection.group()
				save_bio_data(idNum, metadataSection.group(), metafile)
			else:
				print "Couldn't find metadata Section."
			inFile.close()
	
	outfile.close()

if __name__ == "__main__":
	extract_mov_files(sys.argv[1], sys.argv[2], sys.argv[3])

	
