#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Martijn van Leeuwen'
__email__ = 'info@voc-electronics.com'

import os
import sys
import time
import spidev
import RPi.GPIO as GPIO
import subprocess
import threading
import math
import smbus
import datetime

from Adafruit_BMP import BMP085
import Adafruit_GPIO.MCP230xx as MCP

sensor = BMP085.BMP085()

gpio = MCP.MCP23017()

print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))
