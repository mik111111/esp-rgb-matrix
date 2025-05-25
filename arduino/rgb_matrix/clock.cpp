#include <NTPClient.h>
#include <Timezone.h>
#include "clock.h"
#include <WiFiUdp.h>

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);
TimeChangeRule CEST = {"CEST", Last, Sun, Mar, 2, 120};     // Central European Summer Time
TimeChangeRule CET = {"CET ", Last, Sun, Oct, 3, 60};       // Central European Standard Time
Timezone CE(CEST, CET);
long clock_clounter = 0;

long get_local_time()
{
    long utc = timeClient.getEpochTime();
    TimeChangeRule *tcr;
    long local = CE.toLocal(utc, &tcr);
    return local;
}

void start_clock()
{
  timeClient.begin();
  timeClient.update();
}

void update_clock()
{
  clock_clounter++;
  if (clock_clounter % 30 == 0)
    timeClient.update();
}
