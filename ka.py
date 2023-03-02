#!/usr/bin/env python3

#Automaadi käivitamise sequence: 
# 1) Desktopil käivitada bash script
# 2) ka.py script käivitab Test.py (peaprogramm) ja mouse_mover.py
# 3) Test.py GUI avanemise ajal liigutatakse hiir alustusnupu kohale et mängu loop alustada
# 4) Käsitsi läbida üks mäng, et jõuda alustusekraanile

import os


os.system("sudo killall pigpiod")
os.system("sudo pigpiod")
os.system("python3 Test.py & python3 mouse_mover.py")
