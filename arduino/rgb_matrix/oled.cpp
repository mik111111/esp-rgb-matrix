
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "oled.h"

Adafruit_SSD1306 display(OLED_WIDTH, OLED_HEIGHT, &Wire, OLED_RESET);


void oledPrepare(int16_t x, int16_t y, bool invert)
{
  display.setTextSize(1); 
  display.setTextColor(invert ? BLACK : WHITE, invert ? WHITE : BLACK);
  display.setCursor(x, y);
}

void oledPurge()
{
  display.display();
}

void oledTextNoPurge(int16_t x, int16_t y, const char *text, bool invert)
{
  if (strlen(text) <= 1) {
    Serial.print(text);
  } else {
    Serial.println(text);
  }

  oledPrepare(x, y,invert);
  display.print(text);
  display.setTextColor(WHITE);
}

void oledText(int16_t x, int16_t y, const char *text, bool invert)
{
  oledTextNoPurge(x,y,text,invert);
  display.display();
}

void oledInt(int16_t x, int16_t y, int number, bool invert)
{
  oledPrepare(x, y, invert);
  display.print(number);
  display.setTextColor(WHITE);
  display.display();
}