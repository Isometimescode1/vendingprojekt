#
# Nimetus:      hwtest.py
# Kirjeldus:    temp fail, kus erinevaid GPIOga ja muu riistvaraga seotud asju testida saab 
# Autor:        Hardi Tambets
# Kuupäev:      12.2022
#

#import pigpio
#import sys
import hardware as hw
from time import sleep

LIL_LAG = 0         #kui raspi baud rate-i ei muuda on mingit aeglustust vaja attiny numpadi küljes ei saa muidu hakka
while(1):
    input = hw.get_digit()
    if input == "#":
        break
    print(input)
    
