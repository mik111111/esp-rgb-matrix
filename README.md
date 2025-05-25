# Led 32x32 Matrix 

![physical setup](https://github.com/panjanek/esp-rgb-matrix/blob/2fc2af995d744b665803bd0670991a984f6a42d1/images/nyan.gif "physical setup")
![physical setup](https://github.com/panjanek/esp-rgb-matrix/blob/b7c0791ffc91d8f2bd6cf2ae6a49950e5b408bb4/images/rgb.gif "physical setup")
![Web interface](https://github.com/panjanek/esp-rgb-matrix/blob/b7c0791ffc91d8f2bd6cf2ae6a49950e5b408bb4/images/www.gif "web interface")

## Features:
* Web interface
* REST API
* Low level pixel UDP API
* Python library

## Components:
* ESP 8266 (any board, optionaly with small OLED screen for debugging)
* Pixel booster (3.3V -> 5V)
* 32x32 WS2812B panel (may be combined with smaller panels connected in serie)
* Button
* 5V power supply (50W) 

## Sofware:
* Arduino IDE
* Python

## Compiling Arduino firmware

Use "Generrig esp8266 board" with following config:

![Arduino IDE config](https://github.com/panjanek/esp-rgb-matrix/blob/600e4c4edff6f5ff2f321e7af1ea4d31c9701831/images/arduinoconfig.png "Arduino IDE config")

## Wiring

![Wiring diagram](https://github.com/panjanek/esp-rgb-matrix/blob/a4d4f8c96adbd872e76d5bee97589852e9fabb8b/images/wiring-rgb.png "wiring diagram")
