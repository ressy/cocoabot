#!/usr/bin/env python

# Example GPIO code
# Note difference between "BOARD" and "BCM" options

import time
import os
import RPi.GPIO as GPIO

#PINS = (0, 1, 4, 14) # Specify pins to use, BCM mode
PINS = (3, 5, 7, 8) # Specify pins to use, Board mode
delay = 8 # time delay in seconds

def setup():
	GPIO.setmode(GPIO.BOARD)
	for pin in PINS:
		GPIO.setup(pin, GPIO.OUT)

def applyvalues(values):
	for pin, val in zip(PINS, values):
		GPIO.output(pin, val)

def quit():
	for pin in PINS:
		GPIO.output(pin, GPIO.LOW)

# Set all four pins high, then low.
# Repeat until interrupted.
def main():
	setup()
	while True:
		try:
			print("High...")
			applyvalues([GPIO.HIGH]*4)
			time.sleep(delay/2.0)
			print("Low...")
			applyvalues([GPIO.LOW]*4)
			time.sleep(delay)
		except (KeyboardInterrupt, SystemExit):
			quit()
			break
		finally:
			quit()

if __name__ == "__main__":
	main()
