import wave
from pydub import AudioSegment
from pydub.utils import make_chunks
import numpy
import itertools
import random
import sys
from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance
import os.path

file = "";

if hasattr(sys, 'argv'):
    file = sys.argv[1]
    target = sys.argv[2]
    if not os.path.isfile(file):
        print(f"not a file");

targetFolder = "./scrambled/"

print(file);

def get_wav_frame_count(file_path):
    """
    Returns the number of frames in a WAV file.
    """
    try:
        with wave.open(file_path, 'rb') as wf:
            nframes = wf.getnframes()
            return nframes
    except wave.Error as e:
        print(f"Error opening or reading WAV file: {e}")
        return None

# Example usage:
file_name = file  # Replace with your WAV file path
name = os.path.basename(file)
name = os.path.splitext(name)[0]
print(name)

#try:
#    os.makedirs(targetFolder + name, exist_ok=True)
#    print(f"Folder created successfully or already exists.")
#except OSError as e:
#    print(f"Error creating folder: {e}")

frame_count = get_wav_frame_count(file_name)

if frame_count is not None:
    print(f"The WAV file '{file_name}' has {frame_count} frames.")



def split_audio_into_chunks(file_path, chunk_length_ms):
    """
    Splits an audio file into chunks of equal length using pydub.

    Args:
        file_path (str): The path to the audio file.
        chunk_length_ms (int): The desired length of each chunk in milliseconds.
    """
    try:
        audio = AudioSegment.from_file(file_path)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return

    chunks = make_chunks(audio, chunk_length_ms)
    print(chunks);
    lets = ["a","b","c","d","e"];
    orig = "abcde";
    allChunks = list(itertools.permutations(chunks,5));
    allLets =  list(itertools.permutations(lets,5));
    goodChunks = []

    #make a function out of this and lower the threshold if none found
    for i, s in enumerate(allLets):
        allLets[i]  = "".join(s)
        dist = damerau_levenshtein_distance(allLets[i], orig)    
        if (dist > 4):
           goodChunks.append(allChunks[i])
    print("chuuunks");
    print(len(goodChunks));
    count = 0;
    print(allLets);
    for gchunks in goodChunks:

        combined = AudioSegment.empty()
        for chunk in gchunks:
            combined += chunk
        if target: 
            fn = target + "_" + str(count).zfill(3) + ".wav"
        else:
            fn = targetFolder + name + "/" + name + "_" + str(count).zfill(3) + ".wav"
        print(fn)
        combined.export(fn, format="wav")
        count+= 1
        
    #for i, chunk in enumerate(chunks):
    #    chunk_name = f"chunk_{i}.wav"  # You can customize the naming
    #    print(f"Exporting {chunk_name}")
    #    chunk.export(chunk_name, format="wav")  # Or any other format like mp3

# Example usage:
audio_file = file  # Replace with your audio file
audio = AudioSegment.from_file(audio_file)
print(audio.duration_seconds)
secs = audio.duration_seconds * 1000;
print(secs);

chunk_duration = secs / 6  # 10 seconds

split_audio_into_chunks(audio_file, chunk_duration)

