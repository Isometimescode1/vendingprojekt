#
# Nimetus:      hwtest.py
# Kirjeldus:    temp fail, kus erinevaid GPIOga ja muu riistvaraga seotud asju testida saab 
# Autor:        Hardi Tambets
# Kuupäev:      12.2022
#

import pigpio
#import sys
#import hardware as hw
from time import sleep

import leds

LIL_LAG = 0         #kui raspi baud rate-i ei muuda on mingit aeglustust vaja attiny numpadi küljes ei saa muidu hakka
while(1):
    leds.rainbow_cycle(0.001)

    sleep(1)

    print(input)
    
