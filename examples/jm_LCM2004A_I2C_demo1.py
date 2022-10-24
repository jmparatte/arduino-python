#!/usr/bin/python3

from Arduino import *
from Wire import *

from jm_LCM2004A_I2C import jm_LCM2004A_I2C

# ---------------------------------------------------------------------------

Wire.begin()
lcd = jm_LCM2004A_I2C(0x27)
lcd.begin()
#lcd.home()
#lcd.clear()
lcd.write(b'abce')
lcd.home()
delay(1000)
lcd.write(b'ij')
#print(lcd.rd_datareg(), lcd.rd_datareg(), lcd.rd_datareg())
print(lcd.read(), lcd.read(), lcd.read())
delay(1000)
lcd.write(b'k')

custom_font5x8 = bytes([
    0x1F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x1F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F
])
print(lcd.write_cgram(0, 8, custom_font5x8))
print(lcd.set_cursor(0, 3))
for c in range(0x10): lcd.write(c)
