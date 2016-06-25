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
from datetime import datetime

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from Adafruit_BMP import BMP085
import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP

gpio = MCP.MCP23017()
LED_GREEN   = 13
LED_YELLOW  = 12
LED_RED     = 11
LED_BLUE    = 14
LED_WHITE   = 15

gpio.setup(LED_BLUE, GPIO.OUT)
gpio.setup(LED_WHITE, GPIO.OUT)
gpio.setup(LED_RED, GPIO.OUT)
gpio.setup(LED_YELLOW, GPIO.OUT)
gpio.setup(LED_GREEN, GPIO.OUT)

gpio.output(LED_BLUE, 1)
time.sleep(.5)
gpio.output(LED_BLUE, 0)
time.sleep(.5)
gpio.output(LED_WHITE, 1)
time.sleep(.5)
gpio.output(LED_WHITE, 0)
time.sleep(.5)
gpio.output(LED_RED, 1)
time.sleep(.5)
gpio.output(LED_RED, 0)
time.sleep(.5)
gpio.output(LED_YELLOW, 1)
time.sleep(.5)
gpio.output(LED_YELLOW, 0)
time.sleep(.5)
gpio.output(LED_GREEN, 1)
time.sleep(.5)
gpio.output(LED_GREEN, 0)