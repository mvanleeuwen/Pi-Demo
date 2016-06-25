#!/usr/bin/python
# Example using an RGB character LCD connected to an MCP23017 GPIO extender.
import time

import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP


# Define MCP pins connected to the LCD.
lcd_d4        = 2
lcd_d5        = 3
lcd_d6        = 4
lcd_d7        = 5
lcd_en        = 1
lcd_rs        = 0
lcd_bl        = None

# Alternatively specify a 20x4 LCD.
lcd_columns = 20
lcd_rows    = 4

#def clean_display():

# Initialize MCP23017 device using its default 0x20 I2C address.
gpio = MCP.MCP23017()

# Alternatively you can initialize the MCP device on another I2C address or bus.
# gpio = MCP.MCP23017(0x24, busnum=1)

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_bl, gpio=gpio)

lcd.clear()
lcd.home()

# Print a two line message
lcd.message('Hello\nworld!')

# Wait 5 seconds
time.sleep(3.0)

# Demo showing the cursor.
lcd.clear()
lcd.show_cursor(True)
lcd.message('Show cursor')

time.sleep(3.0)

# Demo showing the blinking cursor.
lcd.clear()
lcd.blink(True)
lcd.message('Blink cursor')

time.sleep(3.0)

# Stop blinking and showing cursor.
lcd.show_cursor(False)
lcd.blink(False)

# Demo scrolling message right/left.
lcd.clear()
message = 'Scroll'
lcd.message(message)
for i in range(lcd_columns-len(message)):
    time.sleep(0.5)
    lcd.move_right()
for i in range(lcd_columns-len(message)):
    time.sleep(0.5)
    lcd.move_left()

lcd.clear()
lcd.message('Goodbye!')
lcd.home()