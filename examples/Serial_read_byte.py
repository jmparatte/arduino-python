#!/usr/bin/python3

from Arduino import *

# ===================

Serial.begin()

while True:
    c = Serial.read()
    if c!=-1:
        Serial.println(c)
    if c==27:
        break # <ESC> ?

    delay(1)

Serial.end()
