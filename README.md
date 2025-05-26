# Programmable and hackable RGB Led 32x32 Matrix 

![gif animation](https://github.com/panjanek/esp-rgb-matrix/blob/2fc2af995d744b665803bd0670991a984f6a42d1/images/nyan.gif "gif animation")
![audio display](https://github.com/panjanek/esp-rgb-matrix/blob/aabbcbba27b0b82aa1bab2a1f2d544c8b58a9e62/images/audio.gif "audio display")

![Web interface](https://github.com/panjanek/esp-rgb-matrix/blob/ffc95c94f9b5d970e469c997543260db35100f33/images/www2.gif "web interface")

![uploaded gif](https://github.com/panjanek/esp-rgb-matrix/blob/aabbcbba27b0b82aa1bab2a1f2d544c8b58a9e62/images/mario.gif "uploaded gif")
![clock mode](https://github.com/panjanek/esp-rgb-matrix/blob/aabbcbba27b0b82aa1bab2a1f2d544c8b58a9e62/images/clock.gif "clock mode")

![physical setup](https://github.com/panjanek/esp-rgb-matrix/blob/a0d0e468b642d425ff72234df3bcf2b6b95213a1/images/setup.png "physical setup")

## Features:
* Web interface (with GIF upload)
* REST API
* Low level bitmap streaming UDP API
* Python library
* Fits perfectly into IKEA 32x32cm picture frame :)

## Components:
* ESP 8266 (any board, optionaly with small OLED screen for debugging)
* Pixel booster (3.3V -> 5V)
* 32x32 WS2812B panel (may be combined from smaller panels connected in series)
* Button
* 5V power supply (~50W) 

## Sofware:
* Arduino IDE
* Python

## Compiling Arduino firmware

Use "Generrig esp8266 board" with following config:

![Arduino IDE config](https://github.com/panjanek/esp-rgb-matrix/blob/600e4c4edff6f5ff2f321e7af1ea4d31c9701831/images/arduinoconfig.png "Arduino IDE config")

## Wiring

![Wiring diagram](https://github.com/panjanek/esp-rgb-matrix/blob/52fab240a53717839f5bfc24dc8ca9efc6c62c83/images/wiring-rgb.png "wiring diagram")
