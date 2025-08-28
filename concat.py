from pydub import AudioSegment
import random
import sys
import os
import json


f = open('numbers.json')
data = json.load(f)


r = random.SystemRandom()

def shortSilence():
    slip = r.randint(-25,75)
    dur = 250 + slip
    return AudioSegment.silent(duration=dur)

def longSilence():
    slip = r.randint(-75,75)
    dur = 1500 + slip
    return AudioSegment.silent(duration=dur)

def orchestrate(files):
    btime = 2500 + r.randint(-500,500)
    buffer = AudioSegment.silent(duration=btime)


    combined = AudioSegment.empty() + buffer

    for infile in files:
        if not os.path.exists(infile):
            print("missing file")
            sys.exit()
        combined += shortSilence() + AudioSegment.from_wav(infile)

    combined += longSilence()

    for infile in files:
        if not os.path.exists(infile):
            print("missing file")
            sys.exit()
        combined += shortSilence() + AudioSegment.from_wav(infile)

    combined += buffer
        
    return combined

def evenOut(left, right):
    print("⚖️🤹🏻⚖️🤹🏻")
    ldur = len(left)
    rdur = len(right)
    difference = abs(ldur - rdur)
    if ldur > rdur:
        print("left bigger")
        target = "right"
    elif rdur > ldur:
        print("right bigger")
        target = "left"
    else:
        print("they match")

    print(ldur, rdur, target)

    print("adding ", str(difference), "to ", target)
    print("🛑🛑🛑")
    if target == "right":
        right += AudioSegment.silent(duration=difference)
    elif target == "left":
        left += AudioSegment.silent(duration=difference)
    print(len(left), len(right))
    print("🍏🍏🍏")
    if len(left) != len(right):
        evenOut(left, right)
    return left, right



mono_left, mono_right = evenOut(orchestrate(data["left"]), orchestrate(data["right"]))
print(len(mono_left), len(mono_right))
#stereo_sound = AudioSegment.from_mono_audiosegments(mono_left, mono_right)
mono_left.export("left.wav", format="wav")
mono_right.export("right.wav", format="wav")



