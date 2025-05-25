import cv2
import numpy as np
import PIL
from PIL import Image, ImageFont, ImageDraw 
from rgb_array import RgbArray
import time

rgb = RgbArray("192.168.1.134")
gif = Image.open("../../tmp/nyan3.gif")

data = rgb.gif_to_bytearray(gif, margin=50, adjust_colors=2.0)
print(f"bytes after convertion: {len(data)}")
with open("defaultgif.c", "w") as txt_file:
    txt_file.write("#include \"pgmspace.h\"\r\n")
    txt_file.write(f"static const unsigned char default_gif[] PROGMEM = {{")
    for i in range(len(data)):
        b = data[i]
        txt_file.write(f"{b}")
        if i!=len(data)-1:
            txt_file.write(',')
    txt_file.write("};")

print("starting udp transmission")
while True:
    rgb.send_gif_udp(gif, margin=50)
