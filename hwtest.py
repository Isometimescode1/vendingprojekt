import pigpio
import sys
from time import sleep

# Connect to pigpiod daemon START PIGPIO FROM TERMINAL WITH "sudo pigpiod", will probably cause problems......
pi = pigpio.pi()

if pi != 0:
    print("Pigpio korras: ", pi)
else:
    print("Pigpio-ga on probleeme")

DIR = 26     # Direction GPIO Pin
STEP = 20    # Step GPIO Pin
ENABLE = 21  # GPIO pin of enable

# Set up pins as an output
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)
pi.set_mode(ENABLE, pigpio.OUTPUT)

pigpio.pulse(ENABLE, ENABLE, 100)



# ------------   NELI NUPPU   ----------------------------------------------------------------------------------------
#Nuppude GPIO-d
NUPP1 = 17
NUPP2 = 27
NUPP3 = 22
NUPP4 = 5

#dictionary to return NUPP nr instead of gpio nr
dix = {
    17 : "NUPP1",
    27 : "NUPP2",
    22 : "NUPP3",
    5 : "NUPP4"
}

# Set up pins as an input
pi.set_mode(NUPP1, pigpio.INPUT)
pi.set_mode(NUPP2, pigpio.INPUT)
pi.set_mode(NUPP3, pigpio.INPUT)
pi.set_mode(NUPP4, pigpio.INPUT)
#software debouncing
pi.set_glitch_filter(NUPP1, 50000)
pi.set_glitch_filter(NUPP2, 50000)
pi.set_glitch_filter(NUPP3, 50000)
pi.set_glitch_filter(NUPP4, 50000)

#holds the value of the most recently pressed button
pressed = 0

# callback function
def button_press(gpio, level, tick):
    print("Vajutati nuppu:", dix[gpio], ", tõus:", level, ", aeg: ", tick)     #kas töötab ka mitme nupuga korraga???
    pressed = dix[gpio]
    return pressed

#peale nupu lugemist võiks 'pressed' muutuja nullida, idk kas nii saab...
def reset_button():
    pressed = 0
    return pressed

cb1 = pi.callback(NUPP1, pigpio.FALLING_EDGE, button_press)
cb2 = pi.callback(NUPP2, pigpio.FALLING_EDGE, button_press)
cb3 = pi.callback(NUPP3, pigpio.FALLING_EDGE, button_press)
cb4 = pi.callback(NUPP4, pigpio.FALLING_EDGE, button_press)


 # this will keep the program running forever
try:
    while(1):
        pi.write(STEP, 0)
        sleep(1)
        pi.write(STEP, 1)
        sleep(1)
except KeyboardInterrupt:
    sys.exit(0)