

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_NeoPixel.h>

#include <glcdfont.c>
#include <gfxfont.h>
#include <Fonts/FreeMono9pt7b.h>
#include <Fonts/FreeMono12pt7b.h>
#include <Fonts/FreeMonoBold18pt7b.h>
#include <Fonts/FreeSerif9pt7b.h>
#include <Fonts/FreeSerif12pt7b.h>
#include <Fonts/FreeSerif18pt7b.h>

#include "pixels.h"

inline GFXglyph *pgm_read_glyph_ptr(const GFXfont *gfxFont, uint8_t c) {
#ifdef __AVR__
  return &(((GFXglyph *)pgm_read_pointer(&gfxFont->glyph))[c]);
#else
  return gfxFont->glyph + c;
#endif //__AVR__
}

inline uint8_t *pgm_read_bitmap_ptr(const GFXfont *gfxFont) {
#ifdef __AVR__
  return (uint8_t *)pgm_read_pointer(&gfxFont->bitmap);
#else
  return gfxFont->bitmap;
#endif //__AVR__
}

Adafruit_NeoPixel pixels(NUMPIXELS, DATA_PIN, NEO_GRB + NEO_KHZ800);
int16_t pixels_indexes[WIDTH*HEIGHT];

// *******************************************
// This function compute pixel index for NeoPixel library based on x,y coordinates
// Tweak this function to adapt to specific LED arrays configuration when connected in series 
// *******************************************
int compute_pixel_index(int x, int y)
{
  if (x<0 || y < 0 || x >= WIDTH || y >= HEIGHT)
    return NUMPIXELS;
  
  if (y < SEGMENT_HEIGHT) {
    return 3*SEGMENT_NUMPIXELS + (x) * SEGMENT_HEIGHT + (x%2==0 ? (y) : (7-y));
  } else if (y < SEGMENT_HEIGHT*2) {
    return 2*SEGMENT_NUMPIXELS + (SEGMENT_WIDTH-1-x) * SEGMENT_HEIGHT + (x%2==0 ? (y-SEGMENT_HEIGHT) : (7-(y-SEGMENT_HEIGHT)));
  } else if (y < SEGMENT_HEIGHT *3) {
    return 1*SEGMENT_NUMPIXELS + (x) * SEGMENT_HEIGHT + (x%2==0 ? (y-2*SEGMENT_HEIGHT) : (7-(y-2*SEGMENT_HEIGHT)));
  } else {
    return 0*SEGMENT_NUMPIXELS + (SEGMENT_WIDTH-1-x) * SEGMENT_HEIGHT + (x%2==0 ? (y-3*SEGMENT_HEIGHT) : (7-(y-3*SEGMENT_HEIGHT)));
  }
}

void init_pixel_indexes()
{
    for(int x=0; x<WIDTH; x++)
    {
      for(int y=0; y<HEIGHT; y++)
      {
        pixels_indexes[(y<<5)+x] = compute_pixel_index(x, y);
      }
    }
}

int get_pixel_index(int x, int y)
{
  if (x<0 || y < 0 || x >= WIDTH || y >= HEIGHT)
    return NUMPIXELS;
  
  return pixels_indexes[(y<<5)+x];
}

void set_pixel(int x, int y, int r, int g, int b)
{
    pixels.setPixelColor(get_pixel_index(x, y), r, g, b);
}

void set_pixel(int x, int y, uint32_t c)
{
  if (c == -1)
    c = Adafruit_NeoPixel::ColorHSV( ((x+y) * 65536) / (WIDTH+HEIGHT), 255, 255);
  pixels.setPixelColor(get_pixel_index(x, y), c);
}

void draw_rect(int x, int y, int w, int h, uint32_t c)
{
  if (c == -1)
    c = Adafruit_NeoPixel::ColorHSV( ((x+y) * 65536) / (WIDTH+HEIGHT), 255, 255);

  for(int xx=x; xx<x+w; xx++)
    for(int yy=y; yy<y+h; yy++)
      pixels.setPixelColor(get_pixel_index(xx, yy), c);
}

void fill_rect(int x1, int y1, int x2, int y2, uint32_t color)
{
  if (x1 < 0)
    x1 = 0;
  if (x2 >= WIDTH)
    x2 = WIDTH-1;
  if (y1 < 0)
    y1 = 0;
  if (y2 >= HEIGHT)
    y2 = HEIGHT-1;
  for(int x=x1; x<=x2; x++)
    for(int y=y1; y<=y2; y++)
      set_pixel(x,y,color);
}

int draw_char(const GFXfont *gfxFont, int16_t x, int16_t y, unsigned char c, uint32_t color, uint32_t bg)
{
  if (!gfxFont) 
  {
    for (int8_t i = 0; i < 5; i++) 
    { 
      uint8_t line = pgm_read_byte(&font[c * 5 + i]);
      for (int8_t j = 0; j < 8; j++, line >>= 1) 
      {
        if (line & 1) 
        {
          set_pixel(x + i, y + j, color);
        } else {
          set_pixel(x + i, y + j, bg);
        }
      }
    }

    for(int vy = y; vy < y+8; vy++)
        set_pixel(x + 5, vy, bg);

    return 6;
  } 
  else 
  {
    c -= (uint8_t)pgm_read_byte(&gfxFont->first);
    GFXglyph *glyph = pgm_read_glyph_ptr(gfxFont, c);
    uint8_t adv = (uint8_t)pgm_read_byte(&glyph->xAdvance);
    if (x < -WIDTH || x > WIDTH)
        return adv;
        
    uint8_t *bitmap = pgm_read_bitmap_ptr(gfxFont);
    uint16_t bo = pgm_read_word(&glyph->bitmapOffset);
    uint8_t w = pgm_read_byte(&glyph->width), h = pgm_read_byte(&glyph->height);
    int8_t xo = pgm_read_byte(&glyph->xOffset), yo = pgm_read_byte(&glyph->yOffset);
    uint8_t xx, yy, bits = 0, bit = 0;
    int16_t xo16 = 0, yo16 = 0;

    for (yy = 0; yy < h; yy++) {
      for (xx = 0; xx < w; xx++) {
        if (!(bit++ & 7)) {
          bits = pgm_read_byte(&bitmap[bo++]);
        }
        if (bits & 0x80) {
          set_pixel(x + xo + xx, y + yo + yy, color);
        }
        bits <<= 1;
      }
    }

    return adv;
  }
}

int get_char_width(const GFXfont *gfxFont, char c)
{
    uint8_t first = pgm_read_byte(&gfxFont->first), last = pgm_read_byte(&gfxFont->last);
    if ((c >= first) && (c <= last)) { 
      GFXglyph *glyph = pgm_read_glyph_ptr(gfxFont, c - first);
      return pgm_read_byte(&glyph->xAdvance);
    }
    else {
      return 0;
    }
}

int get_text_width(const GFXfont *gfxFont, const char *str) 
{
  uint8_t c;
  int w = 0;
  while ((c = *str++)) {
    w = w + get_char_width(gfxFont, c);
  }

  return w;
}

const GFXfont* get_font_ptr(int font_nr)
{
  if (font_nr == 1) {
    return &FreeSerif9pt7b;
  } else if (font_nr == 2) {
    return &FreeSerif12pt7b;
  } else if (font_nr == 3) {
    return &FreeMonoBold18pt7b;   // FreeMono18pt7b FreeSerif18pt7b FreeMonoBold18pt7b
  } else {
    return NULL;
  }
}

void draw_text(int16_t x, int16_t y, int font_nr, const char *text, uint32_t color, uint32_t bg)
{
  int dy = 0;
  int h = 8;
  const GFXfont *gfxFont = get_font_ptr(font_nr);
  if (font_nr == 1) {
    dy = 12;
    h = 16;
  } else if (font_nr == 2) {
    dy = 18;
    h = 24;
  } else if (font_nr == 3) {
    dy = 24;
    h = 32;
  }

  if (font_nr > 0)
  {
    fill_rect(x, y, x+get_text_width(gfxFont, text), y+h, bg);
  }

  for(int i=0; i<strlen(text); i++)
  {
    int adv = draw_char(gfxFont, x, y+dy, text[i], color, bg);
    x = x + adv;
  }
}


