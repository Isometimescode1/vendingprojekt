#
# Nimetus:      hwtest.py
# Kirjeldus:    temp fail, kus erinevaid GPIOga ja muu riistvaraga seotud asju testida saab 
# Autor:        Hardi Tambets
# Kuupäev:      12.2022
#

import pigpio
#import sys
import hardware as hw
from time import sleep
import pyautogui
print(pyautogui.size())

pyautogui.moveTo(960, 1000, duration = 6)
pyautogui.click(960, 1000)
