#!/usr/bin/python3

from Arduino import *
from Wire import *

from jm_LCM2004A_I2C import *

lcd = jm_LCM2004A_I2C()

Wire.begin()
lcd.begin()
# write "Hello World!" 4 times...
lcd.set_cursor(0, 0)
lcd.print("Hello World!")
lcd.set_cursor(2, 1)
lcd.print("Hello World!")
lcd.set_cursor(4, 2)
lcd.print("Hello World!")
lcd.set_cursor(6, 3)
lcd.print("Hello World!")
# read 4 written rows from lcd and print it...
for row in range(4):
    lcd.set_cursor(0, row)
    print('"' + ''.join([chr(lcd.read()) for _ in range(20)]) + '"')
