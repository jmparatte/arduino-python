#!/usr/bin/python3

from Arduino import *
from Wire import *

from jm_LCM2004A_I2C import jm_LCM2004A_I2C

Wire.begin()
lcd = jm_LCM2004A_I2C()
lcd.begin()

# write 4 pages of 64 chars to lcd, one after one...
for page in [0x00, 0x40, 0x80, 0xC0]:
    
    # write 4 rows to lcd...
    for row in [0x00, 0x10, 0x20, 0x30]:
        
        # write row to lcd...
        lcd.set_cursor(0, row//0x10)
        lcd.print("{0:02X}".format(page + row))
        lcd.print(' ')
        for i in range(0x00, 0x08):
            lcd.write(page + row + i)
        lcd.print(' ')
        for i in range(0x08, 0x10):
            lcd.write(page + row + i)
            
    # read 4 written rows from lcd... 
    for row in [0x00, 0x10, 0x20, 0x30]:
        
        # read written row from lcd and print it...
        lcd.set_cursor(0, row//0x10)
        print(''.join([
            (lambda c: ('-' if c<32 or c>=127 else chr(c)))(lcd.read())
            for _ in range(20)
        ]))

    delay(1000)
    print()
