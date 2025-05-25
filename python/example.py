import cv2
import numpy as np
import PIL
from PIL import Image, ImageFont, ImageDraw 
from rgb_array import RgbArray
import time

IP = "192.168.1.134"

rgb = RgbArray(IP, debug=True)    #init connection
rgb.set_brightness(20)            #set brightness
rgb.clear(16,32,48)               #clear with color
rgb.set_pixel(0,0,255,0,0)        #set single pixel
time.sleep(1)

#clear and write some texts
rgb.clear(0,0,0)                  
rgb.text("TEST", x=4)
rgb.text("green", x=1, y=8, r=0, g=255, b=0)
rgb.text("red", x=7, y=16, r=255, g=0, b=0)
rgb.text("blue", x=4, y=24, r=0, g=255, b=255)
time.sleep(2)

#draw rectasngles
rgb.rect(8,8,16,16, 0,255,0)
rgb.rect(12,12,8,8, 255,0,0)
time.sleep(2)


gif = Image.open("../../tmp/132C_trans.gif")
data = rgb.gif_to_bytearray(gif, margin=50, adjust_colors=2.0)
while True:
    rgb.send_gif_udp(gif, margin=50, delay=0.05)

