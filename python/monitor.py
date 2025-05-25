import math
import time
from rgb_array import RgbArray
import psutil
import subprocess as sp

rgb = RgbArray("192.168.1.134")

def run_command(command):
    val = sp.run(['powershell', '-Command', command], capture_output=True).stdout.decode("ascii")
    return float(val.strip().replace(',', '.'))

def get_intel_gpu_percent():
    gpu_usage_cmd = r'(((Get-Counter "\GPU Engine(*engtype_3D)\Utilization Percentage").CounterSamples | where CookedValue).CookedValue | measure -sum).sum'
    load = run_command(gpu_usage_cmd)
    print(load)
    return load

def show(y, txt, percent, txt_color1, txt_color2, bar_color, bar_offset = 0):
    rgb.text(txt, x=0, y=y, r=txt_color1[0], g=txt_color1[1], b=txt_color1[2])
    percent_txt = " ?"
    if percent is not None:
        if percent < 0:
            percent = 0
        if percent > 99:
            percent = 99
        percent_txt = f"{str(round(percent)).rjust(2)}"
    rgb.text(percent_txt, x=20, y=y, r=txt_color2[0], g=txt_color2[1], b=txt_color2[2])
    w = 0
    rest = 0
    if percent is not None:
        w = math.floor(32*percent / 100)
        rest = (percent - (w*100/32)) / (100/32)
        #print(rest)        
        if w < 0:
            w = 0
    rgb.rect(0, y+8+bar_offset, w, 2, r=bar_color[0], g=bar_color[1], b=bar_color[2])
    rgb.rect(w, y+8+bar_offset, 1, 2, r=round(bar_color[0]*rest), g=round(bar_color[1]*rest), b=round(bar_color[2]*rest))
    rgb.rect(w+1, y+8+bar_offset, 32-w, 2, r=0, g=0, b=0)


get_intel_gpu_percent()

rgb.clear()
while True:
    show(0, "cpu", psutil.cpu_percent(interval=1), (0,48, 0), (0, 255, 0) , (0, 255, 0))
    show(10, "mem", psutil.virtual_memory().percent, (0,0, 48), (0, 0, 255) , (0, 0, 255))
    show(21, "gpu", get_intel_gpu_percent(), (48, 0, 48), (255, 0, 255) , (255, 0, 255), bar_offset=1)
    time.sleep(0.1)
    