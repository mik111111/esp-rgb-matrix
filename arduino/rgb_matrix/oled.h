#ifndef _OLED_H
#define _OLED_H

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define OLED_WIDTH 128  
#define OLED_HEIGHT 64  

#define OLED_RESET -1        
#define OLED_ADDRESS 0x3C 

extern Adafruit_SSD1306 display;

void oledPurge();
void oledPrepare(int16_t x, int16_t y, bool invert = false);
void oledTextNoPurge(int16_t x, int16_t y, const char *text, bool invert = false);
void oledText(int16_t x, int16_t y, const char *text, bool invert = false);
void oledInt(int16_t x, int16_t y, int number, bool invert = false);

#endif 