#!/usr/bin/env python

import os, sys, shutil

def copy_sample(source_dir, speaker_id, lang_path, out_filename):
	source_filename = source_dir+"speaker"+speaker_id+".wav"
	if os.path.exists(source_filename):
		shutil.copyfile(source_filename, lang_path + out_filename)
		return 1
	return 0

def male_or_female(split_bio_lines, eng_id):
	speaker_bio_lines = [sl for sl in split_bio_lines if int(sl[0]) == int(eng_id)]
	speaker_bio = speaker_bio_lines[0]
	if 'female' in speaker_bio[5]:
		return 'f'
	else:
		return 'm'

def get_eng_wavs():
	id_str = open('english_ids.txt', 'r').read()
	formatted_ids = ''.join([c for c in id_str if c.isalnum() or c.isspace()])
	eng_ids = formatted_ids.split()
	bio_lines = open('bio.out').readlines()
	split_bio_lines = [line.split('\t') for line in bio_lines]
	maleCounter = 0
	femaleCounter = 0
	for eng_id in eng_ids:
		gender = male_or_female(split_bio_lines, eng_id)
		if 'm' in gender:
			maleCounter += 1
			copy_sample('wav_files/', eng_id, 'english_wav_files/', 'english-m'+str(maleCounter)+".wav")
		else:
			femaleCounter += 1
			copy_sample('wav_files/', eng_id, 'english_wav_files/', 'english-f'+str(femaleCounter)+".wav")

if __name__ == "__main__":
	get_eng_wavs()

