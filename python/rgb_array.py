import requests
import cv2
import sys
import numpy as np
import PIL
from PIL import Image, ImageFont, ImageDraw 
import socket
import time
import math
import random
import colorsys


class RgbArray:
    def __init__(self, ip, debug = False):
        self.ip = ip
        self.url = f"http://{ip}"
        self.udp_port = 1234
        self.http_timeout = 5
        self.width = 32
        self.height = 32
        self.debug = debug

    def set_pixel(self, x, y, r, g, b):
        response = requests.post(self.url+"/pixel", {"x":x, "y":y, "r":r, "g":g, "b":b}, timeout=self.http_timeout)
        if  self.debug:
            print(response.content)
            
    def rect(self, x, y, w, h, r, g, b):
        response = requests.post(self.url+"/rect", {"x":x, "y":y, "w":w, "h":h, "r":r, "g":g, "b":b}, timeout=self.http_timeout)
        if  self.debug:
            print(response.content)
            
    def set_brightness(self, b):
        response = requests.post(self.url+"/settings", {"brightness":b}, timeout=self.http_timeout)
        if  self.debug:
            print(response.content)
        
    #name: "none", "matrix", "rainbow",
    def effect(self, name, brightness=255, speed=1.0, text=""):
        response = requests.post(self.url+"/effect", {"name":name, "brightness":brightness, "speed":speed, "text":text}, timeout=self.http_timeout)
        if  self.debug:
            print(response.content)
        
    def text(self, text, x=0, y=0, r=255, g=255, b=255):
        response = requests.post(self.url+"/text", {"x":x, "y":y, "text":text, "r":r, "g":g, "b":b}, timeout=self.http_timeout)
        if  self.debug:
            print(response.content)
        
    def clear(self, r=0, g=0, b=0):
        response = requests.post(self.url+"/clear", {"r":r, "g":g, "b":b}, timeout=self.http_timeout)
        if  self.debug:
            print(response.content)
    
    def image_to_binary_packet(self, img, y, lines):
        data = bytearray()
        data.append(ord('R'))
        data.append(ord('G'))
        data.append(ord('B'))
        data.append(0)
        data.append(y%256)
        for y in range(y, y+lines):
            for x in range(self.width):
                r, g, b = img.getpixel((x, y))
                data.append(r)
                data.append(g)
                data.append(b)
        return data
        
    def adjust_color(self, x, level):
        if level == 1.0:
            return x
        else:
            f = x / 128.0;  
            mx =  math.pow(2.0, level)
            f = math.pow(f, level)
            c = round(f*256 / mx)
            if c<0:
                c = 0
            if c>255:
                c = 255;
            return c;
        
    def image_to_bytearray(self, img, adjust_colors = 1.0):
        data = bytearray()
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = img.getpixel((x, y))
                data.append(self.adjust_color(r,adjust_colors))
                data.append(self.adjust_color(g,adjust_colors))
                data.append(self.adjust_color(b,adjust_colors))
        return data
        
    def gif_to_bytearray(self, gif, margin = 0, adjust_colors = 2.0):
        data = bytearray()
        img = Image.new(mode="RGB", size=(32, 32))
        img.paste( (0,0,0), (0, 0, img.size[0], img.size[1]))
        gif.seek(0)
        try:
            while True:
                print(f"frame={gif.tell()}, size={gif.size}")
                source = gif
                w = gif.size[0]
                h = gif.size[1]
                if w!=h:
                    m = min(w,h)
                    if w>h:
                        source = gif.crop(((w-h)/2+margin, 0+margin, w-(w-h)/2-margin, h-margin))
                    else:
                        source = gif.crop((0+margin, (h-w)/2+margin, w-margin, h-(h-w)/2)-margin)
                else:
                    source = gif.crop((margin, margin, w-margin, h-margin))
                Image.Image.paste(img, source.resize((32,32), resample=PIL.Image.BICUBIC), box=(0,0,32,32))
                frame = self.image_to_bytearray(img, adjust_colors)
                data.extend(frame)
                gif.seek(gif.tell() + 1)
        except EOFError:
            return data
            
    def send_gif_bytearray_udp(self, data, frame_size, delay = 0.1):
        frame_count = int(len(data) / frame_size)
        header = bytearray()
        header.append(ord('R'))
        header.append(ord('G'))
        header.append(ord('B'))
        header.append(0)
        header.append(0)
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        for f in range(frame_count):
            frame = data[f*frame_size:(f+1)*frame_size]
            packet = header + frame
            sentcount = sock.sendto(packet, (self.ip, self.udp_port))
            if  self.debug:
                print(f"[{f}]: sent={sentcount}.", end='')
            sys.stdout.flush()
            time.sleep(delay)    
            
    def send_gif_udp(self, gif, margin = 0, delay = 0.1):
        data = self.gif_to_bytearray(gif, margin)
        frame_size = self.width * self.height * 3;
        self.send_gif_bytearray_udp(data, frame_size, delay)

    def send_image_udp(self, img):
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        data = self.image_to_binary_packet(img, 0, self.height)
        sentcount = sock.sendto(data, (self.ip, self.udp_port))
        if  self.debug:
            print(f"{sentcount}.", end='')
        sys.stdout.flush()
      
    def scroll_text(self, text):
        img = PIL.Image.new(mode="RGB", size=(self.width, self.height))
        size = 28
        w = 14
        font = ImageFont.truetype("arial.ttf", size)
        t = 0
        for x in range(self.width, len(text)*-14, -1):
            t = t + 1
            img.paste( (0,0,0), (0, 0, img.size[0], img.size[1]))
            draw = ImageDraw.Draw(img)  
            draw.text((x, -2), text, font = font, align ="left", fill=(255,255,255))  
            pixels = img.load()
            for ix in range(self.width):
                for iy in range(self.height):
                    r,g,b = pixels[ix, iy]
                    if r > 0:
                        h = ((t+ix+iy) % 100) / 100.0
                        r2,g2,b2 = colorsys.hsv_to_rgb(h, 1.0, r/256.0)
                        pixels[ix, iy] = (round(r2*255), round(g2*255), round(b2*255))
            self.send_image_udp(img)
            time.sleep(0.02)


