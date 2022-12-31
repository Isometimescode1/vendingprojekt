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
    
