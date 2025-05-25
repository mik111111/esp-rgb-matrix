#ifndef _PIXELS_H
#define _PIXELS_H

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_NeoPixel.h>

// data: D1 = GPIO5
#define DATA_PIN 5

#define WIDTH 32
#define HEIGHT 32
#define NUMPIXELS 1024
#define SEGMENTS_COUNT 4
#define SEGMENT_WIDTH 32
#define SEGMENT_HEIGHT 8
#define SEGMENT_NUMPIXELS 256

extern Adafruit_NeoPixel pixels;

int compute_pixel_index(int x, int y);
void init_pixel_indexes();
int get_pixel_index(int x, int y);
void set_pixel(int x, int y, int r, int g, int b);
void set_pixel(int x, int y, uint32_t c);
void draw_rect(int x, int y, int w, int h, uint32_t c);
void fill_rect(int x1, int y1, int x2, int y2, uint32_t color);
int draw_char(const GFXfont *gfxFont, int16_t x, int16_t y, unsigned char c, uint32_t color, uint32_t bg = 0);
int get_char_width(const GFXfont *gfxFont, char c);
int get_text_width(const GFXfont *gfxFont, const char *str);
const GFXfont* get_font_ptr(int font_nr);
void draw_text(int16_t x, int16_t y, int font_nr, const char *text, uint32_t color, uint32_t bg = 0);

#endif 
