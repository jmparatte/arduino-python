#!/usr/bin/python3

from Arduino import *

# ===================

Serial.begin()

n = 0
while True:
    c = Serial.read()
    if c==27: break # <ESC> ?
    if c!=-1: # valid char ?
        Serial.print(n) # approximativ milliseconds time
        Serial.print(' ')
        Serial.println(c) # read char

    delay(10)
    n += 10

Serial.end()
