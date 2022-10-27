#!/usr/bin/python3

from Arduino import *

# ===================

Serial.begin()

n = 0
while True:
    c = Serial.read()
    if c==27:
        break # <ESC> ?
    if c!=-1:
        Serial.print(n)
        Serial.print(' ')
        Serial.println(c)

    delay(1)
    n += 1

Serial.end()
