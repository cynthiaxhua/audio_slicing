# TRANSCRIPTIONS

1. Convert to flac: https://convertio.co/video-converter/
2. Upload to google cloud storage bucket: https://console.cloud.google.com/storage/browser/npr_audio?project=portraits-234615
3. confirm google credentials
export GOOGLE_APPLICATION_CREDENTIALS="/Users/xihua/Documents/Keys/Portraits-de779188c7bd.json"
4. run text_to_long.py to transcribe

# DATA FORMAT

## Full Transcript:
	Text

## Phrase:
File_No. --> dict
	Filename --> text
	Phrase_No. --> dict
		Start --> text
		End --> text
		Text --> text

## Words
Word_Code = File_Phrase_Word (ex: 3_2_1 is the first word of the second phrase of the third file)
	Start
	End
	Word

## Glossary
Word = "text"
	Word_Codes (List)
	 	File_Phrase_Word
		Start
		End
		Year

# CUTTING

make_glossary.py creates a glossary of all terms
gen_audio.py takes a phrase and creates an audio file
cut_by_word.py takes a word and creates an audio file of all instances of that word

# MAKE TSNE's

1. run sort.py to format for tsne's
2. run tsne.py



