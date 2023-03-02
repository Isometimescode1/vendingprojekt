import hardware as hw
from time import sleep

for x in range(10):

	hw.motor_direction(0)
	hw.generate_ramp([ [60, 5],             
					[100, 10],
					[120, 20],
					[140, 90],
					[120, 20],
					[100, 10],
					[60, 5]])
	sleep(3)

