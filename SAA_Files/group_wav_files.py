#!/usr/bin/env python
# Copy .wav files into directory of language-segmented subdirectories.
# Args: [bio information file] [.wavs source dir] [output directory] [number of languages] [s]
# Where s is the maximum number of speaker samples per language, or -1 for
# no limit.

import os, sys, shutil

def get_lang_counts(bio_filename):
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
	return lines, lang_counts

def get_speaker_ids_of_lang(bio_lines, lang):
	speaker_ids = []
	genders = []
	for line in bio_lines:
		tokens = line.split('\t')
		if lang == tokens[2]:
			speaker_ids.append(tokens[0])
			genders.append(tokens[5])
	return speaker_ids, genders

def copy_sample(source_dir, speaker_id, lang_path, out_filename):
	source_filename = source_dir+"speaker"+speaker_id+".wav"
	if os.path.exists(source_filename):
		shutil.copyfile(source_filename, lang_path + out_filename)
		return 1
	return 0

def group_langs(bio_filename, wavs_dir, out_dir, num_langs, samples_per_lang):
	bio_lines, lang_counts = get_lang_counts(bio_filename)
	sorted_keys = sorted(lang_counts, key=lang_counts.get, reverse=True)
	for i in range(num_langs):
		lang = sorted_keys[i+1]
		speaker_ids, genders = get_speaker_ids_of_lang(bio_lines, lang)
		lang_path = out_dir + lang + "/"
		if not os.path.isdir(lang_path):
			os.makedirs(lang_path)
		numMale = numFemale = 0
		numRead = 0
		for j in range(len(speaker_ids)):
			if (not samples_per_lang == -1) and numRead >= samples_per_lang:
				break
			increment = 0
			if genders[j] == 'male':
				numMale += 1
				increment = copy_sample(wavs_dir, speaker_ids[j], lang_path, lang+"-m"+str(numMale)+".wav")
			elif genders[j] == 'female':
				numFemale += 1
				increment = copy_sample(wavs_dir, speaker_ids[j], lang_path, lang+"-f"+str(numFemale)+".wav")
			numRead += increment

if __name__ == "__main__":
	group_langs(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))

