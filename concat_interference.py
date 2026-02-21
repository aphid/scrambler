from pydub import AudioSegment, effects  
import random
import sys
import os
import json


f = open('numbers.json')
data = json.load(f)

r = random.SystemRandom()

def shortSilence():
    slip = r.randint(-250,250)
    dur = 1500 + slip
    return AudioSegment.silent(duration=dur)

def longSilence():
    slip = r.randint(-75,75)
    dur = 3500 + slip
    return AudioSegment.silent(duration=dur)

def orchestrate(files):
    btime = 150 + r.randint(-75,90)
    buffer = AudioSegment.silent(duration=btime)


    combined = AudioSegment.empty() + buffer

    for infile in files:
        #print(infile)
        if not os.path.exists(infile):
            print("missing file")
            sys.exit()
        combined += shortSilence() + effects.normalize(AudioSegment.from_wav(infile))

    combined += longSilence()

    buffer = AudioSegment.silent(duration=btime)
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



#mono_left, mono_right = evenOut(orchestrate(data["left"]), orchestrate(data["right"]))
chorus = orchestrate(data);
chorus.export("interfere.wav", format="wav")



