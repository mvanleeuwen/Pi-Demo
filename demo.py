#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Martijn van Leeuwen'
__email__ = 'info@voc-electronics.com'

'''
# =[ DISCLAIMER ]===============================================================
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ==============================================================================
#
#  App name: demo.py
#
#  Target system:  Linux
#
#  Description: Used to run the display presentation demo using a fully stacked
#               breadboard with LEDS, Sensors and a Character display.
#
# ==============================================================================
# Imports
# ==============================================================================
'''

import time
import RPi.GPIO as GPIO
import datetime

# Import SPI library (for hardware SPI) and MCP3008 library.
#import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from Adafruit_BMP import BMP085
import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP

DEBUG = True

# Sleep Loop settings in seconds.
INITIAL_SLEEP = 10
PROBE_SLEEP = 2
DEFAULT_SLEEP = 5
WAITING_SLEEP = 300
SLEEPING_FOR = 0
MOTION_COUNT = 0

# Define MCP pins connected to the LCD.
lcd_d4 = 2
lcd_d5 = 3
lcd_d6 = 4
lcd_d7 = 5
lcd_en = 1
lcd_rs = 0
lcd_bl = None

# Define LCD column and row size for 20x4 LCD.
lcd_columns = 20
lcd_rows    = 4

# LEDS
LED_GREEN  = 13
LED_YELLOW = 12
LED_RED    = 11
LED_BLUE   = 14
LED_WHITE  = 15

# HC-SR04
TRIG = 22                                  #Associate pin 23 to TRIG
ECHO = 27                                  #Associate pin 24 to ECHO

# Setup GPIO for HC-SR04
GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in
GPIO.output(TRIG, False)                 #Set TRIG as LOW

#10 DOF
sensor = BMP085.BMP085()

# LUX


# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25

#spi = spidev.SpiDev()
#spi.open(0, 0)

# Initialize MCP23017 device using its default 0x20 I2C address.
gpio = MCP.MCP23017()

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                              lcd_columns, lcd_rows, lcd_bl,
                              gpio=gpio)
# Initialize the MCP3008
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


if not mcp:
  print('MCP23017 not found, unable to test the LED layout.')

try:
  gpio.setup(LED_BLUE, GPIO.OUT)
  gpio.setup(LED_WHITE, GPIO.OUT)
  gpio.setup(LED_RED, GPIO.OUT)
  gpio.setup(LED_YELLOW, GPIO.OUT)
  gpio.setup(LED_GREEN, GPIO.OUT)
except Exception:
  print('Error %s', str(Exception.message))
  if mcp:
    message = "Error found: \n" + str(Exception.message)
    lcd.message(message)


def readChannel(channel):
  adc = spi.xfer2([1, (8 + channel) << 4, 0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data


def print_mcp3008_readings():
  print('Reading MCP3008 values, press Ctrl-C to quit...')
  print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} | {8:>4} |'.format(*range(9)))
  print('-' * 64)
  timer = 0
  for timer in range(1, 11):
    # Read all the ADC channel values in a list.
    values = [0]*9
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    # Print the ADC values.
    values[8] = readChannel(0)
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} | {8:>4} |'.format(*values))
    # Pause for half a second.
    time.sleep(1)


def get_lux_reading(results = 0):
  results = mcp.read_adc(0)
  return results


def test_bmp085():
  temp = sensor.read_temperature()
  alti  = sensor.read_altitude()
  pres = sensor.read_sealevel_pressure()
  print('Temp = {0:0.2f} *C'.format(temp))
  print('Pressure = {0:0.2f} Pa'.format(pres))
  print('Altitude = {0:0.2f} m'.format(alti))
  #print('Sealevel Pressure = {0:0.2f} Pa'.format())
  if lcd:
    message = "Temp: {0:3.2f}\nPressure: {0:8.2f}\nAltitude: {0:0.2f} m".format(temp, pres, alti)
    lcd.clear()
    lcd.home()
    lcd.message(message)
    time.sleep(1)


def write_time_lcd():
  now = datetime.datetime.now()
  lcd.message(now.strftime("%d/%m/%Y %H:%M\n"))


def leds_on():
  gpio.output(LED_BLUE, 1)
  gpio.output(LED_WHITE, 1)
  gpio.output(LED_RED, 1)
  gpio.output(LED_YELLOW, 1)
  gpio.output(LED_GREEN, 1)


def leds_off():
  gpio.output(LED_BLUE, 0)
  gpio.output(LED_WHITE, 0)
  gpio.output(LED_RED, 0)
  gpio.output(LED_YELLOW, 0)
  gpio.output(LED_GREEN, 0)


def led_test():
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


def activate_hc_sr04(distance = 0):
  # Distance locked at 400cm.
  pulse_end = 0
  pulse_start = 0
  if DEBUG:
    print('Activating HC-SR04')
  if lcd:
    lcd.clear()
    lcd.home()
    lcd.message('Activating HC-SR04.')

  GPIO.output(TRIG, True)  # Set TRIG as HIGH
  time.sleep(0.00001)  # Delay of 0.00001 seconds
  GPIO.output(TRIG, False)  # Set TRIG as LOW

  while GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW
    pulse_start = time.time()  # Saves the last known time of LOW pulse

  while GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH
    pulse_end = time.time()  # Saves the last known time of HIGH pulse

  pulse_duration = pulse_end - pulse_start  # Get pulse duration to a variable

  distance = pulse_duration * 17150  # Multiply pulse duration by 17150 to get distance
  distance = round(distance, 2)  # Round to two decimal points

  if 2 < distance < 400:  # Check whether the distance is within range
    if DEBUG:
      print "Distance:", distance - 0.5, "cm"  # Print distance with 0.5 cm calibration
    else:
      distance -= 0.5
  else:
    if DEBUG:
      print "Out Of Range"  # display out of range
    distance = 400

  return distance


def get_temp(temperature = 0):
  if sensor:
    try:
      temperature = sensor.read_temperature()
    except Exception:
      # On all Exceptions return -1
      temperature = -1
      pass

  return temperature


def get_pressure(pressure = 0):
  if sensor:
    try:
      pressure = sensor.read_pressure()
    except Exception:
      # On all Exceptions return -1
      pressure = -1
      pass

  return pressure


def get_altitude(alt = 0 ):
  if sensor:
    try:
      alt = sensor.read_altitude()
    except Exception:
      alt = -1
      pass

  return alt


def run_loop():
  cur_temp = get_temp()
  cur_pressure = get_pressure()
  cur_lux = get_lux_reading()


'''
Start initialization routines.
'''
lcd.show_cursor(False)
lcd.home()
lcd.clear()
write_time_lcd()
lcd.message('Welcome.')
time.sleep(2)
lcd.clear()
lcd.home()
write_time_lcd()
if DEBUG:
  print('Starting sensors')
lcd.message('Starting sensors.')
time.sleep(1)
lcd.clear()
lcd.home()
if DEBUG:
  print('Gearing up.')
message = 'Gearing up.'
lcd.message(message)
for i in range(lcd_columns-len(message)):
    time.sleep(0.2)
    lcd.move_right()
for i in range(lcd_columns-len(message)):
    time.sleep(0.2)
    lcd.move_left()
time.sleep(2.0)
lcd.clear()
lcd.home()
message = 'Loading presets.'
if DEBUG:
  print(message)
lcd.message(message)
for i in range(lcd_columns-len(message)):
    time.sleep(0.2)
    lcd.move_right()
for i in range(lcd_columns-len(message)):
    time.sleep(0.2)
    lcd.move_left()
time.sleep(2.0)
lcd.clear()
lcd.home()
try:
  lux = get_lux_reading()
  write_time_lcd()
  if DEBUG:
    print('Testing Lux Sensor.')
  lcd.message('Testing LUX sensor\n')
  lcd.message('Result: ')
  lcd.message(str(lux))
  if DEBUG:
    print('Result: %s' % str(lux))
except Exception as e:
  lcd.message('Unable to get data\nfrom LUX sensor.\n')
  if DEBUG:
    print('ERROR: Unable to retrieve data from LUX sensor.')
  lcd.message(e.message)
time.sleep(2)
lcd.home()
lcd.clear()
write_time_lcd()
if DEBUG:
  print('Starting LED Test.')
lcd.message('Starting LED test.')
led_test()
time.sleep(2)
leds_on()
time.sleep(2)
leds_off()
lcd.home()
lcd.clear()
# Test BMP180
test_bmp085()
time.sleep(2)
lcd.clear()
lcd.home()
lcd.message('All sensors\n'
            'initialized.\n'
            'Play time!')
time.sleep(2)
lcd.clear()
lcd.home()
# Main program loop.
movement_detected = False

'''
The infinite loop
We start with a probe to see if motion is detected to determine if we are going to sleep for 5min
'''
motion = activate_hc_sr04()
if motion < 400:
  SLEEPING_FOR = PROBE_SLEEP
  MOTION_COUNT = 1
else:
  SLEEPING_FOR = WAITING_SLEEP
  MOTION_COUNT = 0

try:
  while True:
    time.sleep(SLEEPING_FOR)
    # Loop infinite and wake on movement detection
    #ToDo: Fixup detection loop.
    motion = activate_hc_sr04()
    if motion < 400:
      if MOTION_COUNT < 4:
        MOTION_COUNT += 1
      else:
        run_loop()
        MOTION_COUNT = 0
        SLEEPING_FOR = WAITING_SLEEP

except KeyboardInterrupt:
  pass

'''
Exit on key press
'''
if DEBUG:
  print('All done.')
  lcd.clear()
  lcd.home()
  lcd.message('All done.')
  time.sleep(2)
  lcd.clear()
  lcd.home()
