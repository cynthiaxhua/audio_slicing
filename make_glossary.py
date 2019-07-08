import json
import os
from pydub import AudioSegment

#reads in transcribed jsons and produces a word-level glossary
def make_glossary():
	for year in range(1999,2009):
		print("processing: " + str(year))
		json_infile = "../Transcriptions/Results/" + str(year) + "/words.json"
		with open(json_infile, 'r') as f:
			data = json.load(f) #produces a dict object
			print("json loaded")
		glossary = dict()
		#iterate over each word in the word json
		for key,value in data.items(): #key is word_code
			word = value['Text'].lower()
			start_time = int(value['Start'] * 1000) # convert to ms
			end_time = int((value['End']) * 1000)
			start_end = str(start_time) + "_" + str(end_time)
			#create an dictionary entry with keys (word_code, start_end)
			entry = dict()
			entry['year'] = year
			entry['start_end'] = start_end
			entry['word_code'] = key #file_no, phrase_no, word_no = key.split("_")
			#add to the glossary
			if word in glossary: #if already an entry
				glossary[word].append(entry)
				#print(word)
				#print(glossary[word])
			else:
				glossary[word] = [entry]
	with open('glossary.json', 'w') as f:
		json.dump(glossary, f)

#create glossary — create a json glossary with info on each word in corpus?
make_glossary()

#read in glossary json file to check 
#with open("glossary.json", 'r') as f:
#	glossary = json.load(f)



