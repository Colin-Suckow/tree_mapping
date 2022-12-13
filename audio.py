"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
import numpy
import os
import json
import audioop

from light import *
import time
from detector import *
import math
from patterns import *

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)


if os.path.isfile('light_pos.json'):
    print("Loading light positions from disk...")
    with open('light_pos.json', 'r') as f:
        points = json.load(f)
    print("Done!")
else:
    print("No light data found. Calculating...")
    points = combine_points(calculate_points("front"), calculate_points("right_side"))
    print("Done! Saving calculated data...")
    with open('light_pos.json', 'w') as f:
        json.dump(points, f)
    print("Done!")

wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# read data
data = wf.readframes(CHUNK)

# play stream (3)
while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)
    # Do all of your DSP processing here i.e. function call or whatever
    rms = audioop.rms(data, 2) / 65535
    def light_func(i):
        r = 0
        g = 0
        b = 0
        if i % 2 == 0:
            r = 0.15
        else:
            g = 0.15
        if points[i] is None:
            pass
        elif 1 - points[i][1] > rms * 3:
            pass
        else:
            if r > 0:
                r = 1
            if g > 0:
                g = 1
        return (int(g * 64), int(r * 64), int(b * 64))

    send_pattern(light_func)
# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()