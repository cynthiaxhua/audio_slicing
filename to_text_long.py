import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import json

def transcribe_gcs_with_word_time_offsets(gcs_uri, filename, file_num):
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding='FLAC',
        sample_rate_hertz=44100,
        audio_channel_count=2,
        language_code='en-US',
        enable_word_time_offsets=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    result = operation.result(timeout=300)

    #printed = ''
    transcript = ''
    phrase_results = dict() #list of phrase_no entries
    word_results = dict() # list of word_code entries
    phrase_count = 0
    for result in result.results:
        phrase_entry = dict()
        alternative = result.alternatives[0]
        transcript += alternative.transcript
        transcript += ' '
        phrase_entry['Text'] = alternative.transcript
        #printed += 'Transcript: {} \n'.format(alternative.transcript)
        #printed += 'Confidence: {} \n'.format(alternative.confidence)
        #print(u'Transcript: {}'.format(alternative.transcript))
        #print('Confidence: {}'.format(alternative.confidence))
        word_count = 0
        for word_info in alternative.words:
            word_code = str(file_num) + "_" + str(phrase_count) + "_" + str(word_count)
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            if word_count == 0:
                phrase_entry['Start'] = start_time.seconds + start_time.nanos * 1e-9
            '''
            print('Word: {}, start_time: {}, end_time: {}, speaker: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))
            printed += 'Word: {}, start_time: {}, end_time: {} \n'.format(
                    word,
                    start_time.seconds + start_time.nanos * 1e-9,
                    end_time.seconds + end_time.nanos * 1e-9)
            '''
            word_entry = dict()
            word_entry['Start'] = start_time.seconds + start_time.nanos * 1e-9
            word_entry['End'] = end_time.seconds + end_time.nanos * 1e-9
            word_entry['Text'] = word_info.word
            word_results[word_code] = word_entry
            word_count += 1
        phrase_entry['Start'] = end_time.seconds + end_time.nanos * 1e-9
        phrase_results[phrase_count] = phrase_entry
        phrase_count += 1
    #printed += 'File Name: {} \n'.format(gcs_uri)
    print("Success with " + gcs_uri)
    return transcript, phrase_results, word_results

#transcribe_gcs_with_word_time_offsets("gs://npr_audio/Test/0.flac")
'''
final_result = ''
for i in range(9,10):
    print(i)
    uri_path = "gs://npr_audio/Test/" + str(i) + '.flac'
    final_result += transcribe_gcs_with_word_time_offsets(uri_path)
    with open('result89.txt', 'w') as f:
        f.write(final_result)
'''
'''
Sentences:
File_No.
    Phrase_No.
        Start
        End
        Text
Words
Word_Code = File_Phrase_Word
    Start
    End
    Word
'''
full_transcript = ''

year = 2002
phrases_json = dict()
words_json = dict()
i = 0
for filename in os.listdir("../Data/full/flac/"+str(year)+"/"):
    try:
        print(filename)
        print(i)
        uri_path = "gs://npr_audio/Full/"+str(year)+"/"+filename
        print("processing file: " + str(uri_path))
        transcript_output, phrase_output, word_output = transcribe_gcs_with_word_time_offsets(uri_path, filename, i)
        full_transcript += transcript_output
        phrases_json[i] = dict()
        phrases_json[i]['phrases'] = phrase_output
        phrases_json[i]['filename'] = filename
        words_json.update(word_output)
        with open(str(year)+"/"+'transcript.txt', 'w') as f:
            f.write(full_transcript)
        with open(str(year)+"/"+'phrases.json', 'w') as f:
            json.dump(phrases_json, f)
        with open(str(year)+"/"+'words.json', 'w') as f:
            json.dump(words_json, f)
        i += 1
    except:
        continue


