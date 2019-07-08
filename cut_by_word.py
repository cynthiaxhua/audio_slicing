import json
import os
from pydub import AudioSegment

#read in file_no and produce the clip start_time, end_time in desired format
def cut(instances,year):
	#load phrases json which has info on file names
	phrases_infile = "../Transcriptions/Results/" + str(year) + "/phrases.json"
	with open(phrases_infile, 'r') as f:
		phrase_data = json.load(f) #produces a dict object
	#iterate over files
	#keep a counter to name audio clips
	i = 0
	for key,value in instances.items():
		try:
			#extract filename from phrases
			filename = phrase_data[key]['filename']
			#load the .wav audio file associated with filename
			wav_infile = filename.split(".")[0] + ".wav"
			audio_file = AudioSegment.from_wav("../Data/full/wav/"+str(year)+"/"+wav_infile)
			#iterate over each instance of the target word in a given audio clip
			for item in value:
				start_time, end_time = item.split("_")
				start_time = int(start_time)
				end_time = int(end_time)
				#clip audio
				audio_segment = audio_file[start_time:end_time]
				#export audio
				audio_outfile = "Clips/" + target_word + "/" + str(year) + "/" + str(i)  + ".wav"
				audio_segment.export(audio_outfile, format="wav")
				print(i)
				i += 1
		except:
			continue
	print('cuts complete')

#returns a list of instances of target word appearing
def find_instances(target, source):
    instances = dict() #referenced by file_no
    #iterate over each word in the word json
    for key,value in source.items():
    	if value['Text'].lower() == target:
    		#print(key)
    		file_no, phrase_no, word_no = key.split("_")
    		start_time = int(value['Start'] * 1000) # convert to ms
    		end_time = int((value['End']) * 1000) + 15
    		start_end = str(start_time) + "_" + str(end_time)

    		if file_no in instances:
    			instances[file_no].append(start_end)
    		else:
    			instances[file_no] = [start_end]
    print("instances found")
    return instances

def combine(infolder, target_word):
	sounds = [] #list of audio sound indata
	for year_folder in os.listdir(infolder + "/"):
		for filename in os.listdir(infolder + "/" + year_folder + "/"):
			try:
				infile = infolder + "/" + year_folder + "/" + filename
				print(infile)
				sound = AudioSegment.from_wav(infile)
				if len(sound) <= 2000:
					sounds.append(sound)
			except:
				continue
	combined = sounds[0] #concatenated outdata
	for i in range(1,len(sounds)):
		combined += sounds[i]
	combined.export("Combined/"+target_word+".wav", format="wav")

target_word = "history"
#year = 2004
for year in range(1999,2009):
	words_infile = "../Transcriptions/Results/" + str(year) + "/words.json"
	with open(words_infile, 'r') as f:
		data = json.load(f) #produces a dict object
		print("json loaded")
		instances = find_instances(target_word,data)
		print(len(instances))
		if not os.path.exists("Clips"):
			os.mkdir("Clips")
		if not os.path.exists("Clips/" + str(target_word)):
			os.mkdir("Clips/" + str(target_word))
		if not os.path.exists("Clips/" + target_word + "/" + str(year)):
			os.mkdir("Clips/" + target_word + "/" + str(year))
		cut(instances,year)

if not os.path.exists("Combined"):
	os.mkdir("Combined")
combine("Clips/"+target_word,target_word)
