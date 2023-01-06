#
# Nimetus:      hwtest.py
# Kirjeldus:    temp fail, kus erinevaid GPIOga ja muu riistvaraga seotud asju testida saab 
# Autor:        Hardi Tambets
# Kuupäev:      12.2022
#

#import pigpio
#import sys
#import hardware as hw
from time import sleep
import os
import threading

#import leds

def caller():
    os.system("sudo python3 -c 'import leds; leds.rainbow_cycle(0.0001)'")
        
t1 = threading.Thread(target=caller)


while(1):
    #os.system("sudo python3 -c 'import leds; leds.rainbow_cycle(0.0001)'")
    t1.start()
    for i in range(10):
        print("i", i)
        sleep(1)
    t1.join()
    os.system("sudo python3 -c 'import leds; leds.rainbow_cycle(0.001)'")
    print("johhaidii")
    for i in range(10):
        print("u", i)
        sleep(1)
