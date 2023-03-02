#
# Nimetus:      hardware.py
# Kirjeldus:    tegeleb Müügiautomaadis Raspberry GPIO külge ühendatuga (samm mootor, lineaartäitur, valgustid, surunupud, numbriklaviatuur), 
# Autor:        Erik Lootus, Hardi Tambets
# Kuupäev:      12.2022
# Kokku laenatud kood viidatud
#


import pigpio
from time import sleep, time


# Connect to pigpiod daemon START PIGPIO FROM TERMINAL WITH "sudo pigpiod", will probably cause problems......
pi = pigpio.pi()
if pi != 0:
    print("Pigpio korras: ", pi)
else:
    print("Pigpioga on probleeme")


# ------------   MOOTOR   ----------------------------------------------------------------------------------------
# INFO https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/
# 1 step = 1.8 deg -> 360/1.8 = 200 steps per rev
MOTOR_STEPS = 200
# transmission ratio 1:10
TRANS_RATIO = 10
# microsteps (200, 400, 800, 1600, 3200) 
MICROSTEPS = 400       #(8x the normal steps)
# number of pocets on wheel = 50
# rotaion needed for one pocket 360/50 = 7.2 deg
# steps needed for one pocket (1600 - 320 steps, 400 - 80 steps)
POCKET_STEPS = MICROSTEPS * TRANS_RATIO / 50
# steps needed for succesful acceleration
ACCEL_STEPS = 35

DIR = 26     # Direction GPIO Pin
STEP = 20    # Step GPIO Pin
ENABLE = 21  # GPIO pin of enable

# Set up pins as an output
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)
pi.set_mode(ENABLE, pigpio.OUTPUT)

# To enable the main motor externally:
def motor_disable(state):
    #low = motor enabled
    #high = motor disabled
    pi.write(ENABLE, state)

# direction change
def motor_direction(dir):
    #high = vastupäeva (hammaka poolt vaadates)
    #low = päripäeva (hammaka poolt vaadates)
    pi.write(DIR, dir)

# Acceleration ramping generation method
def generate_ramp(ramp):
    """Generate ramp wave forms.
    ramp:  List of [Frequency, Steps]
    """
    pi.wave_clear()     # clear existing waves
    length = len(ramp)  # number of ramp levels
    wid = [-1] * length

    # Generate a wave per ramp level
    for i in range(length):
        frequency = ramp[i][0]
        micros = int(500000 / frequency)
        wf = []
        wf.append(pigpio.pulse(1 << STEP, 0, micros))  # pulse on
        wf.append(pigpio.pulse(0, 1 << STEP, micros))  # pulse off
        pi.wave_add_generic(wf)
        wid[i] = pi.wave_create()

    # Generate a chain of waves
    chain = []
    for i in range(length):
        steps = ramp[i][1]
        x = steps & 255
        y = steps >> 8
        chain += [255, 0, wid[i], 255, 1, x, y]

    pi.wave_chain(chain)  # Transmit chain.

# Ramp (freq(Hz), nr of steps)       #RPM = MICROSTEPS / freq * 60   #omega = RPM * 0.10472
# Näidis üles ja alla ramp: Kindlati vaja timmida, kestvus: 3.94 s
#generate_ramp([ [60, 32],             
#	            [80, 64],
#	            [100, 64],
#	            [80, 64],
#	            [60, 32]])


# ------------   MOOTOR endex  ----------------------------------------------------------------------------------------

# ------------   VÄLJUTI   ----------------------------------------------------------------------------------------
PUSH = 25     # Actuator relay 1 (push)
RETRACT = 16     # Actuator relay 2 (retract)

# Set up pins as an output
pi.set_mode(PUSH, pigpio.OUTPUT)
pi.set_mode(RETRACT, pigpio.OUTPUT)

def actuate_cycle():
    # push out
    pi.write(PUSH, 1)
    sleep(4)
    pi.write(PUSH, 0)
    # wait a bit to give ralays some time
    sleep(1)
    # retract the actuator
    pi.write(RETRACT, 1)
    sleep(4)
    pi.write(RETRACT, 0)

def actuate_push():
    # push out
    pi.write(PUSH, 1)
    sleep(4)
    pi.write(PUSH, 0)
    # wait a bit to give ralays some time
    sleep(1)

def actuate_retract():
    # retract the actuator
    pi.write(RETRACT, 1)
    sleep(4)
    pi.write(RETRACT, 0)
    # wait a bit to give ralays some time
    sleep(1)

# ------------   VÄLJUTI endex  ----------------------------------------------------------------------------------------

# ------------   OHUTUSLÜLITI   ----------------------------------------------------------------------------------------
SAFETY = 19     # Safety switch on the fill up hatch
QUALIFIER_TIME = 50000  #microseconds


# Set up pins as an input
pi.set_mode(SAFETY, pigpio.INPUT)
#debouncing
pi.set_glitch_filter(SAFETY, QUALIFIER_TIME)

# callback function
def button_press(gpio, level, tick):
    print("Täitmiskaas lahti:", SAFETY, ", tõus:", level, ", aeg: ", tick)
    return SAFETY

# callback if a button is pressed (like interrupts but lame)
cb0 = pi.callback(SAFETY, pigpio.FALLING_EDGE, button_press)

def kaas_state():       # REAALNE JUHTMESTUS ÕIETI TEHA!!
    # returns 1 if hatch closed
    # returns 0 if hatcj open
    return (pi.read(SAFETY))

# ------------   OHUTUSLÜLITI endex  ----------------------------------------------------------------------------------------

# ------------   NELI NUPPU   ----------------------------------------------------------------------------------------
#Nuppude GPIO-d
NUPP1 = 17
NUPP2 = 27
NUPP3 = 22
NUPP4 = 5
QUALIFIER_TIME = 50000  #microseconds

#dictionary to return NUPP nr instead of gpio nr
dix = {
    17 : 1,
    27 : 3,
    22 : 2,
    5 : 4
}

# Set up pins as an input
pi.set_mode(NUPP1, pigpio.INPUT)
pi.set_mode(NUPP2, pigpio.INPUT)
pi.set_mode(NUPP3, pigpio.INPUT)
pi.set_mode(NUPP4, pigpio.INPUT)
#software debouncing
pi.set_glitch_filter(NUPP1, QUALIFIER_TIME)
pi.set_glitch_filter(NUPP2, QUALIFIER_TIME)
pi.set_glitch_filter(NUPP3, QUALIFIER_TIME)
pi.set_glitch_filter(NUPP4, QUALIFIER_TIME)


class Nupud():
    def __init__(self, pressed):
        self.vajutatud = pressed    #holds the value of the most recently pressed button

nupud = Nupud(0)

# callback function
def button_press(gpio, level, tick):
    print("Vajutati nuppu:", dix[gpio], ", tõus:", level, ", aeg: ", tick)     #kas töötab ka mitme nupuga korraga???
    nupud.vajutatud = dix[gpio]
    return nupud.vajutatud

#peale nupu lugemist võiks 'PRESSED' muutuja nullida, idk kas nii saab...
def reset_button():
    nupud.vajutatud = 0
    return nupud.vajutatud

# Siin reaalselt oodatakse nupuvajutust kuni timeout (s) täis saab
def get_input(timeout, period):
    ajalõpp = time() + timeout
    while time() < ajalõpp:
        if nupud.vajutatud != 0:
            return nupud.vajutatud
        sleep(period)
    print("Liiga kaua sai oodatud: nupu input timeout!")
    return 0
  

# callbacks if a button is pressed (like interrupts but lame)
cb1 = pi.callback(NUPP1, pigpio.FALLING_EDGE, button_press)
cb2 = pi.callback(NUPP2, pigpio.FALLING_EDGE, button_press)
cb3 = pi.callback(NUPP3, pigpio.FALLING_EDGE, button_press)
cb4 = pi.callback(NUPP4, pigpio.FALLING_EDGE, button_press)

# ------------   NELI NUPPU endex   ----------------------------------------------------------------------------------------

# ------------   LEDs   ----------------------------------------------------------------------------------------

#neopixel? ei tea kuidas see GPIO-ga kokku mängib
#vaja reaalselt kätte saada üks

# ------------   LEDs endex   ----------------------------------------------------------------------------------------


# ------------   I2C for KEYPAD   ----------------------------------------------------------------------------------------
# Muudetud SparkFun Qwiic_keyboard.py
# Set Raspi i2c baud to something low, boot/config.txt 10000baud

#VÄGA KAHTLANE KAS KÕIK TÖÖTAB NII NAGU PEAKS

_DEFAULT_NAME = "Keypad"
I2C_ADDRESS = [0x4B]

FIFO_SIZE = 16
INTERRUPT_PIN = 6

# Register codes for the keypad
KEYPAD_ID       = 0x00
KEYPAD_VERSION1 = 0x01
KEYPAD_VERSION2 = 0x02
KEYPAD_BUTTON   = 0x03
KEYPAD_TIME_MSB = 0x04
KEYPAD_TIME_LSB = 0x05
KEYPAD_UPDATE_FIFO = 0x06
KEYPAD_CHANGE_ADDRESS = 0x07

class QwiicKeypad(object):
    """
    QwiicKeypad
        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :return: The QwiicKeypad device object.
        :rtype: Object
    """
    # Constructor
    device_name         = _DEFAULT_NAME
    available_addresses = I2C_ADDRESS
    handle              = 0

    # Constructor
    def __init__(self, address=None):

        # Did the user specify an I2C address?
        self.address = address if address is not None else self.available_addresses[0]
        
    # ------------------------------------------------------------------
    # Initialize the system/validate the board.
    def begin(self):
        """
            Initialize the operation of the Keypad module
            :return: Returns true of the initializtion was successful, otherwise False.
            :rtype: bool
        """
        print("aadress: ", self.address)
        self.handle = pi.i2c_open(1, self.address)
        print("handle: ", self.handle)


    # ---------------------------------------------------------------
    # Is an actual board connected to our system?
    def is_connected(self):
        """
            Determine if a Keypad device is conntected to the system..
            :return: True if the device is connected, otherwise False.
            :rtype: bool
        """
        if self.handle != 0:
            return 1
        else:
            return 0

    connected = property(is_connected)

    #----------------------------------------------------------------
    # Returns the button at the top of the stack (aka the oldest button)
    def get_button(self):
        """
            Returns the button at the top of the stack (aka the oldest button).
            The return value is the 'ascii' value of th key pressed. To convert
            to a character, use the python char() function.
            :return: The next button value
            :rtype: byte as integer
        """
        value = 0

        # bus can throw an issue
        try:
            value = pi.i2c_read_byte_data(self.handle, KEYPAD_BUTTON)
        except IOError:
            print("IO error")
            pass

        return (value)

    #----------------------------------------------------------------
    # Returns the number of milliseconds since the current button in FIFO was pressed.
    def time_since_pressed(self):
        """
            Returns the number of milliseconds since the current button in FIFO was pressed.
            :return: The elapsed time since button was pressed
            :rtype: integer
        """
        MSB = pi.i2c_read_byte_data(self.handle, KEYPAD_TIME_MSB)
        LSB = pi.i2c_read_byte_data(self.handle, KEYPAD_TIME_LSB)
        return (MSB << 8) | LSB

    #----------------------------------------------------------------
    # "commands" keypad to plug in the next button into the registerMap
    #  note, this actually sets the bit0 on the updateFIFO register

    def update_fifo(self):
        """
        "commands" keypad to plug in the next button into the registerMap
        note, this actually sets the bit0 on the updateFIFO register
        :return: No return value
        """
        # set bit0, commanding keypad to update fifo
        pi.i2c_write_byte_data(self.handle, KEYPAD_UPDATE_FIFO, 0x01)

#eemaldab suvalise klaviatuurivajutused FIFO puhvrist
def clear_fifo():
    for x in range(FIFO_SIZE):
        numpad.update_fifo()
        numpad.get_button()


# Siin luuake numpadi klass, mida kasutatakse kuni reboodini
numpad = QwiicKeypad()
numpad.begin()
TRELLID = 35        #ASCII '#' = 35 decimal
LIL_LAG = 0         #kui raspi baud rate-i ei muuda on mingit aeglustust vaja attiny numpadi küljes ei saa muidu hakkama

# ootab kuni numpadil miskit vajutatakse ja siis tagastab selle char-ina
def get_digit():
    klahv = 0
    while klahv != TRELLID:
        numpad.update_fifo()
        klahv = numpad.get_button()
        if klahv == TRELLID:
            break
        elif klahv != 0x00:
            #print("Sisestati:", klahv)
            break
        else:
            #if klahv == 0, ootame nupuvajutust
            sleep(LIL_LAG)
    return chr(klahv)
# ------------   I2C for KEYPAD endex   ----------------------------------------------------------------------------------------


#-------------  Kombod  --------------------------------------------------------------------------------------------------------
def väljasta():
    print("Ratta indekseerimine")
    motor_direction(0)
    generate_ramp([ [60, 64],             
	            [80, 64],
	            [100, 64],
	            [80, 64],
	            [60, 64]])
    sleep(5)
    print("Ratas indekseeritud")
    print("lükkamise algus")
    actuate_cycle()
    print("lükatud")


# Kõik ratta keeramise ja manageerimisega seotu
class Wheel:
    def __init__(self):
        self.pockets = 50
        self.last_ejected = 0
        self.candy_remaining = 50
        self.current_pocket = 1
        self.place_in_sequence = 0

    rotationSequence = {
        1: 25
        2: 12
        3: 25
        4: 14
    }
    
    # ei luba current poceti väärtuseks midagi 50-st suuremat
    def advance_index(i):
        self.current_pocket += i
        if self.current_pocket > 50:
            self.current_pocket = self.current_pocket - 50

    # Keerab etteantud arvu taskuid edasi
    def advance_x(x):
        steps = POCKET_STEPS * x
        speedSteps = steps - (2 * ACCEL_STEPS)
        timeToComplete = 2 + speedSteps/140*1.3  #time to do the steping + a little bit

        print("Ratta indekseerimine")
        motor_direction(0)
        generate_ramp([ [60, 5],             
                        [100, 10],
                        [120, 20],
                        [140, speedSteps]
                        [120, 20],
                        [100, 10],
                        [60, 5]])

        sleep(timeToComplete)
        advance_index(x)
        print("Ratas indekseeritud")


    # Keerab etteantud taskuni
    def adcvance_to(x):
        if x > self.current_pocket:
            advance_x(x - self.current_pocket)
        elif x < self.current_pocket:
            advance_x(self.pockets - self.current_pocket + x)
        else:
            print("Ära jama, see tasku on juba ees")

    # hoiab ratast tasakaalus keeramise ajal
    # Wheel starts at pocket 1
    # Turning sequence after emptying the first pocket is +25 -> +12 -> +25 -> +13 +shift 1
    # This succesfully and in a balanced fashin manages to dispence 48 pieces of candy
    # Candy in pockets 50 and 25 remain and need to be extraced manually
    def balancedRotate():
        if self.candy_remaining > 2:
            match self.place_in_sequence:
                case 0 or 1:
                    keera_x(rotationSequence[self.place_in_sequence])
                    advance_index(rotationSequence[self.place_in_sequence])
                    self.place_in_sequence = 2
                case 2:
                    keera_x(rotationSequence[self.place_in_sequence])
                    advance_index(rotationSequence[self.place_in_sequence])
                    self.place_in_sequence += 1
                case 3:
                    keera_x(rotationSequence[self.place_in_sequence])
                    advance_index(rotationSequence[self.place_in_sequence])
                    self.place_in_sequence += 1
                case 4:
                    keera_x(rotationSequence[self.place_in_sequence])
                    advance_index(rotationSequence[self.place_in_sequence])
                    self.place_in_sequence = 1
                case _:
                    print("Midagi läks metsa. balancedRotate case_")
        elif self.candy == 2:


                

Ratas = Wheel()

