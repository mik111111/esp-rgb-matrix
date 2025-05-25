#ifndef _CLOCK_H
#define _CLOCK_H

#include <NTPClient.h>
#include <Timezone.h>
#include <WiFiUdp.h>

long get_local_time();
void start_clock();
void update_clock();

#endif