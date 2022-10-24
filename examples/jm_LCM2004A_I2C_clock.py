#!/usr/bin/python3

from Arduino import *
from Wire import *

import jm_time as time

from jm_LCM2004A_I2C import jm_LCM2004A_I2C

lcd = jm_LCM2004A_I2C()

clock_custom_font5x8 = bytes([
#0:
    0b00001,
    0b00011,
    0b00011,
    0b00111,
    0b00111,
    0b01111,
    0b01111,
    0b11111,
#1:
    0b10000,
    0b11000,
    0b11000,
    0b11100,
    0b11100,
    0b11110,
    0b11110,
    0b11111,
#2:
    0b11111,
    0b01111,
    0b01111,
    0b00111,
    0b00111,
    0b00011,
    0b00011,
    0b00001,
#3:
    0b11111,
    0b11110,
    0b11110,
    0b11100,
    0b11100,
    0b11000,
    0b11000,
    0b10000,
#4:
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
#5:
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
#6:
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
#7:
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000
])
#lcd.write_cgram(0, 8, clock_custom_font5x8)

# LCD characters to draw Clock digits
# ===================================
#0: Clock LCD custom character 0
#1: Clock LCD custom character 1
#2: Clock LCD custom character 2
#3: Clock LCD custom character 3
#4: Clock LCD custom character 4
#5: Clock LCD custom character 5
#6: Clock LCD custom character 6
#7: Clock LCD custom character 7
S = 0x20 # LCD Space character
B = 0xFF # LCD Block character

clock_digits_font4x4 = bytes([
#0: '0'
    0, B, B, 1,
    B, S, S, B,
    B, S, S, B,
    2, B, B, 3,
#1: '1'
    S, 0, B, S,
    S, S, B, S,
    S, S, B, S,
    0, B, B, 3,
#2: '2'
    0, B, B, 1,
    S, S, 0, 3,
    S, 0, 3, S,
    0, B, B, 3,
#4: '3'
    0, B, B, 1,
    S, S, 0, 3,
    S, S, 2, 1,
    2, B, B, 3,
#4: '4'
    S, S, 0, 3,
    S, 0, 3, S,
    0, B, B, 3,
    S, S, 3, S,
#5: '5'
    0, B, B, 3,
    B, B, B, 1,
    S, S, S, B,
    2, B, B, 3,
#6: '6'
    S, 0, B, 3,
    0, 3, S, S,
    B, 3, 2, 1,
    2, 1, 0, 3,
#7: '7'
    0, B, B, 1,
    S, S, 0, 3,
    S, 0, 3, S,
    0, 3, S, S,
#8: '8'
    0, 3, 2, 1,
    2, 1, 0, 3,
    0, 3, 2, 1,
    2, 1, 0, 3,
#9: '9'
    0, 3, 2, 1,
    2, 1, 0, B,
    S, S, 0, 3,
    0, B, 3, S,
#10: ':'
    S, 0, 1, S,
    S, 2, 3, S,
    S, 0, 1, S,
    S, 2, 3, S,
#11: ' '
    S, S, S, S,
    S, S, S, S,
    S, S, S, S,
    S, S, S, S,
])

def clock_digit_display(digit, digit_col):
    for row in range(4):
        lcd.set_cursor(4*digit_col, row)
        lcd.write(clock_digits_font4x4[4*(4*digit+row):4*(4*digit+row)+4])

def clock_colon_display(state, digit_col):
    if state: # colon shown ?
        digit = 10 #10: ':'
    else: # colon cleared
        digit = 11 #11: ' '
    clock_digit_display(digit, digit_col)

def clock_hh_mm_display(hh, mm, colon):
    clock_digit_display(hh//10, 0)
    clock_digit_display(hh%10, 1)
    clock_colon_display(colon, 2)
    clock_digit_display(mm//10, 3)
    clock_digit_display(mm%10, 4)

def clock():
    global lcd
    hh_ = -1
    mm_ = -1
    while True:
        # get localtime to display...
        #t = time.time()
        #ms = int((t - int(t))*1000)
        tms = time.time_ns()//1000000
        t = tms//1000
        ms = tms%1000
        lt = time.localtime(t)
        hh = lt[3]
        mm = lt[4]
        # check if display is allready connected else...
        if not lcd.connected():
            hh_ = -1
            mm_ = -1
            # try to (re)connect...
            lcd.begin()
            # clear screen...
            lcd.clear_display()
            # load custom fonts...
            lcd.write_cgram(0, 8, clock_custom_font5x8)
        # display clock if lcd connected...
        if lcd.connected():
            # if hh_mm has changed...
            if (not hh_==hh or not mm_==mm):
                # display hh_mm...
                clock_hh_mm_display(hh, mm, ms<500)
                # update internal if lcd connected...
                if lcd.connected():
                    hh_ = hh
                    mm_ = mm
            else:
                # blink colon...
                clock_colon_display(ms<500, 2)
        # wait/synchronize/display clock on next 500ms slot...
        delay((1000 - ms)%500)

if __name__=="__main__":
    Wire.begin()
    clock()
