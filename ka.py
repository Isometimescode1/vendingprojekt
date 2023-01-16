import os


os.system("sudo killall pigpiod")
os.system("sudo pigpiod")
os.system("python3 Test.py & python3 hwtest.py")