import wave
from pydub import AudioSegment
from pydub.utils import make_chunks
import numpy
import itertools
import random

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
file_name = "test.wav"  # Replace with your WAV file path
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
    #random.shuffle(chunks)
    
    comb = list(zip(chunks, lets))
    
    random.shuffle(comb)

    chunks[:], lets[:] = zip(*comb)
    print(lets);
    combined = AudioSegment.empty()
    for chunk in chunks[0]:
        combined += chunk
    
    combined.export("test_scramb.wav", format="wav")

    #for i, chunk in enumerate(chunks):
    #    chunk_name = f"chunk_{i}.wav"  # You can customize the naming
    #    print(f"Exporting {chunk_name}")
    #    chunk.export(chunk_name, format="wav")  # Or any other format like mp3

# Example usage:
audio_file = "test.wav"  # Replace with your audio file
audio = AudioSegment.from_file(audio_file)
print(audio.duration_seconds)
secs = audio.duration_seconds * 1000;
print(secs);

chunk_duration = secs / 5  # 10 seconds

split_audio_into_chunks(audio_file, chunk_duration)

