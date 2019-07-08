import json
import os
from pydub import AudioSegment
import string
import random

#create glossary — create a json glossary with info on each word in corpus
#see make_glossary.py
if not os.path.exists("Generated"):
	os.mkdir("Generated")

target_phrase = "this day in history, america was freed"
#strip punctuation and capitalization 
target_phrase = target_phrase.translate(str.maketrans('', '', string.punctuation))
target_phrase = target_phrase.lower()

#break target phrase into list of words
target_words = target_phrase.split(" ")
num_words = len(target_words)

#read in glossary
with open("glossary.json", 'r') as f:
	glossary = json.load(f)

#find words
i = 0
for word in target_words:
	#look up in glossary
	possible_instances = glossary[word]
	instance = random.choice(possible_instances)
	year = instance['year']
	word_code = instance['word_code']
	start_end = instance['start_end']
	#get filename from the phrases.json file (which is keyed by year)
	phrases_infile = "../Transcriptions/Results/" + str(year) + "/phrases.json"
	with open(phrases_infile, 'r') as f:
		phrase_data = json.load(f)
	#get file number
	file_no, phrase_no, word_no = word_code.split("_")
	filename = phrase_data[file_no]['filename']
	#read in wav file
	wav_infile = filename.split(".")[0] + ".wav"
	audio_file = AudioSegment.from_wav("../Data/full/wav/"+str(year)+"/"+wav_infile)
	#cut from file
	start_time, end_time = start_end.split("_")
	start_time = int(start_time)
	end_time = int(end_time)
	#clip audio
	audio_segment = audio_file[start_time:end_time]
	#export audio
	audio_outfile = "Generated/" + str(i)  + ".wav"
	audio_segment.export(audio_outfile, format="wav")
	print(i)
	i += 1

#combine words
sounds = [] #list of audio sound indata
i = 0
for i in range(0, num_words): 
	"Generated/" + str(i)  + ".wav"
	sound = AudioSegment.from_wav(infile)
	if len(sound) <= 3000: #filter out errors
		sounds.append(sound)
	except:
		continue
combined = sounds[0] #concatenated outdata
for i in range(1,len(sounds)):
	combined += sounds[i]
combined.export("phrase.wav", format="wav")


