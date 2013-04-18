#!/usr/bin/env python
# 
# Read in commands and manage control of motors via GPIO
# 2013-03-23
# 
# Pipe stuff:
# http://stackoverflow.com/questions/6241260/python-named-pipes-problem
# http://www.roman10.net/named-pipe-in-linux-with-a-python-example/

import time
import os
import errno
import RPi.GPIO as GPIO

# Constants
DELTA_T = 0.01 # Time step per cycle, seconds
TTL = 50 # number of cycles to keep output for
PIPE_FILENAME = '/tmp/motorcmds' # named pipe to read in commands
UID = 33 # UID to write to pipe (www-data)
GID = 33 # GID to write ot pipe (www-data)
PINS = (3, 5, 7, 8) # Specify pins to use (board-wise)
CMDS = {} # Combinations of pins to set high
CMDS["F"]  = [1, 0, 1, 0] # [0, 2] # forward
CMDS["B"]  = [0, 1, 0, 1] # [1, 3] # backward
CMDS["L"]  = [0, 0, 1, 0] # [2]    # left forward
CMDS["R"]  = [1, 0, 0, 0] # [0]    # right forward
CMDS["LT"] = [0, 1, 1, 0] # [1, 2] # left turn
CMDS["RT"] = [1, 0, 0, 1] # [0, 3] # right turn
# Pin:   Effect on motor:
# 0      left forward
# 1      left backward
# 2      right forward
# 3      right backward

def setup():
	# Set pins relative to board, and in output mode
	GPIO.setmode(GPIO.BOARD)
	for pin in PINS:
		GPIO.setup(pin, GPIO.OUT)
	# Create named pipe
	try:
		os.remove(PIPE_FILENAME)
	except OSError:
		pass
	os.mkfifo(PIPE_FILENAME)
	# Give ownership to the user who'll write to it
	cmd_pipe = os.open(PIPE_FILENAME, os.O_RDONLY | os.O_NONBLOCK)
	os.fchown(cmd_pipe, UID, GID)
	return cmd_pipe

def readcmds(pipe):
	try:
		lines = os.read(pipe, 1024).rstrip().split("\n")
	except OSError, exc:
		if exc.errno == errno.EAGAIN:
			return ['']
		else:
			raise exc
	return lines

def parsecmds(lines):
	cmd = [GPIO.LOW] * 4
	if lines[0]:
		for line in lines:
			try:
				cmd = CMDS[line]
				print("%s -> %s" % (line, str(cmd)))
			except KeyError:
				print('ignoring bad command "%s"' % line)
	return cmd

def applyvalues(values):
	for pin, val in zip(PINS, values):
		GPIO.output(pin, val)

def zeropins():
	for pin in PINS:
		GPIO.output(pin, GPIO.LOW)

def quit(cmd_pipe):
	print("Exiting...")
	zeropins()
	os.close(cmd_pipe) # Close the pipe file
	os.remove(PIPE_FILENAME) # ...and delete it

def main_loop(cmd_pipe):
	try:
		countdown = TTL
		while True:
			t1 = time.time()
			lines = readcmds(cmd_pipe)
			if lines[0]:
				values = parsecmds(lines)
				applyvalues(values)
				if sum(values):
					countdown = TTL
			countdown -= 1
			if countdown <= 0:
				zeropins()
			t2 = time.time()
			time.sleep(DELTA_T)
	except (KeyboardInterrupt, SystemExit):
		pass
	finally:
		quit(cmd_pipe)

# Go!
cmd_pipe = setup()
main_loop(cmd_pipe)
