#!/bin/python
import sys, os, random, subprocess

def choose_wav_file(wav_dir, langs):
    lang = random.choice(langs)
    lang_dir = os.path.join(wav_dir, lang)
    wav_file = random.choice(os.listdir(lang_dir))
    return os.path.join(lang_dir, wav_file)

def ask_user_to_continue():
    answer = raw_input("Press enter to guess an accent or q to quit: ")
    return len(answer) == 0 or answer.lower() != "q"

def get_lang(path):
    filename = path.split("/")[-1]
    return filename.split("-")[0].capitalize()

def print_options(langs):
    for i in range(len(langs)):
        print "{} = {}".format(str(i+1).ljust(2), langs[i].capitalize())

def isValidNumber(response, max_val):
    try:
        val = int(response)
        return val in range(1, max_val + 1)
    except ValueError:
        return False

def wait_for_response(wav_file, langs):
    process = subprocess.Popen(["afplay", wav_file])
    response = ""
    max_lang = len(langs)
    while True:
        response = raw_input("Choose a language (1-"+str(max_lang)+") or press 'P' to play again: ")
        if isValidNumber(response, max_lang):
            process.terminate()
            return langs[int(response) - 1]
        elif len(response) > 0 and response[0].lower() == "p":
            process.terminate()
            process = subprocess.Popen(["afplay", wav_file])

def accent_guesser_loop(wav_dir):
    langs = os.listdir(wav_dir)
    while ask_user_to_continue():
        wav_file = choose_wav_file(wav_dir, langs)
        lang = get_lang(wav_file)
        print_options(langs)
        response = wait_for_response(wav_file, langs)
        if response.lower() == lang.lower():
            print "\nCongratulations! That was indeed {}.\n".format(lang.capitalize())
        else:
            print "\nSorry! That was actually {}, not {}.\n".format(lang.capitalize(), response.capitalize())



if __name__ == "__main__":
    wav_dir = "grouped_wav_files" if len(sys.argv) <= 1 else sys.argv[1]
    accent_guesser_loop(wav_dir + "/")