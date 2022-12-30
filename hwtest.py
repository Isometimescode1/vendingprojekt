import pigpio
import sys
import hardware as hardware
from time import sleep



 # this will keep the program running forever
try:
    print("here goes")
    while(1):
        sleep(1)

except KeyboardInterrupt:
    sys.exit(0)