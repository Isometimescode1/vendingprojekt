import hardware as hw
from time import sleep

print("current pocket:", hw.ratas.current_pocket)
#hw.motor_direction(1)
for i in range(50):

    hw.balancedRotate()
    sleep(1)
    print("nyyd lükkan")
    hw.actuate_cycle()
    sleep(10)

#hw.actuate_cycle()

#hw.balancedRotate()

print("current pocket:", hw.ratas.current_pocket)
#print("rotation sequence", hw.ratas.rotationSequence[hw.ratas.place_in_sequence])

#hw.balancedRotate()

print("current pocket:", hw.ratas.current_pocket)

#hw.balancedRotate()

print("current pocket:", hw.ratas.current_pocket)

#hw.balancedRotate()

print("current pocket:", hw.ratas.current_pocket)