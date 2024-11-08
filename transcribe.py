import vosk
import pyaudio
import json
import os
from close import predefined_phrases,get_closest_match, priorities
import numpy as np

# Here I have downloaded this model to my PC, extracted the files 
# and saved it in local directory
# Set the model path
model_path = "vosk-model-small-en-us-0.15"
# Initialize the model with model-path
model = vosk.Model(model_path)



#if you don't want to download the model, just mention "lang" argument 
#in vosk.Model() and it will download the right  model, here the language is 
#US-English
#model = vosk.Model(lang="en-us")

def draw_ui(recognised_text, match_text, score, intensity, threshold=100):
    os.system('cls')
    print(f"\tRecognised text:\n\t{recognised_text}")
    if(score > threshold):
        print(f"\tMatched phrase: {match_text}")
        print(f"\tMatched score: {score}")
        print(f"\tIntensity calculated: {intensity}")

rec = vosk.KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192)

def rms(signal):
    signal = np.frombuffer(signal, dtype=np.int16)
    a2 = np.sum(np.power(signal,2))/len(signal)
    return np.sqrt(a2)

output_file_path = "./transcripts/recognized_text.txt"
os.system('cls')
print("Listening for speech. Say 'Terminate' to stop.")
while True:
    data = stream.read(4096)#read in chunks of 4096 bytes
    if rec.AcceptWaveform(data):#accept waveform of input voice
        # Parse the JSON result and get the recognized text
        result = json.loads(rec.Result())
        recognized_text = result['text']
        intensity = rms(data)

        
        # Write recognized text to the file
        with open(output_file_path, "a") as output_file:
            output_file.write(recognized_text + "\n")
        if(recognized_text != ""):
            closest_match, score = get_closest_match(recognized_text, predefined_phrases)
            intensity = intensity*priorities[closest_match]
            draw_ui(recognized_text,closest_match, score, intensity)
        
        
        if "terminate" in recognized_text.lower():
            print("Termination keyword detected. Stopping...")
            break
# Stop and close the stream
stream.stop_stream()
stream.close()

# Terminate the PyAudio object
p.terminate()