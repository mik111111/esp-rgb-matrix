import pyaudio
import wave
import numpy as np
from scipy import signal
from scipy.io import wavfile
import struct
from rgb_array import RgbArray
from PIL import Image, ImageFont, ImageDraw 
import timeit
import math

rgb = RgbArray("192.168.1.134")

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
index = -1
for i in range(p.get_device_count()): 
    dev = p.get_device_info_by_index(i)
    if "Mix" in dev["name"]: 
        index = int(dev["index"])
        print(dev)
  
# select your audio mixed device, trial and error, read
# on windows try: https://shankhanilborthakur.medium.com/recording-system-audio-in-windows-10-using-pyaudio-1559f3e1b64f  
index = 1                                    
print(f"selected device index: {index}")


p = pyaudio.PyAudio()
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                input_device_index = index,
                frames_per_buffer = CHUNK)

print("* recording")


while True:
    print(".",end="")
    start = timeit.timeit()
    data = stream.read(CHUNK, exception_on_overflow=False)
    #print(f"acquiring data    : {(timeit.timeit() - start):0.6f}")
    
    start = timeit.timeit()
    data_unpacked = struct.unpack(f'<{len(data)//2}h', data) 
    #print(f"unpacking         : {(timeit.timeit() - start):0.6f}")
    
    start = timeit.timeit()
    f, P = signal.periodogram(data_unpacked, 44100, nfft=128) 
    #print(f"fft               : {(timeit.timeit() - start):0.6f}")

    start = timeit.timeit()
    img = Image.new(mode="RGB", size=(32, 32))
    img.paste( (0,0,0), (0, 0, img.size[0], img.size[1]))
    pixels = img.load()
    draw = ImageDraw.Draw(img)   
    m = 5000
    d = round(len(data_unpacked)/32)
    fscale = m / 16.0
    ascale = 10 * m / 8
    for x in range(32):
        v = math.floor(P[x]/fscale)
        if (v > 15):
            v = 15
        if v < 0:
            v = 0
        draw.rectangle((x, 15-v, x+1, 15), fill ="#00ff00")
        if 15-v-1 >= 0:
            r = round((P[x] - v*fscale)*255.0 / fscale)
            if r < 0:
                r = 0
            if r > 255:
                r = 255
            pixels[x,15-v-1] = (0,r,r)
        part = data_unpacked[x*d:x*d+d]
        a = max(part) - min(part)
        h = math.floor(a / ascale)
        if h<0:
            h = 0
        if h > 8:
            h = 8
        draw.rectangle((x, 24-h, x+1, 24+h), fill ="#ffff00")
        if h < 7:
           r = round((a - h*ascale) * 255.0 / ascale)
           if r < 0:
               r = 0
           if r > 255:
               r = 255
           pixels[x,24-h-1] = (r,r//4,0)
           pixels[x,24+h+1] = (r,r//4,0)    
    #print(f"drawing          : {(timeit.timeit() - start):0.6f}")
    
    start = timeit.timeit()
    rgb.send_image_udp(img)
    #print(f"udp              : {(timeit.timeit() - start):0.6f}")

