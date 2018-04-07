#! /usr/bin/python

import serial
#import pyfirmata

from time import sleep

bluetoothSerial = serial.Serial("/dev/rfcomm0", baudrate=115200)


from pyfirmata import Arduino, util
board = Arduino('/dev/rfcomm0')

board.digital[4].write(255)
