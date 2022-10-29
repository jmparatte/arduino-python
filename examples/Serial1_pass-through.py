#!/usr/bin/python3

from Arduino import *

# ===================

# create Serial1 object...

if implementation=='cpython':
    from PythonSerial import *
    Serial1 = PythonSerial(SERIAL1_COM_PORT)
elif implementation=='micropython':
    from MicropythonSerial import *
    Serial1 = MicropythonSerial(SERIAL1_UART_NUM, SERIAL1_TX_PIN, SERIAL1_RX_PIN)
else:
    pass

# ===================

Serial.begin(115200)
Serial1.begin(115200)

while True:
    # echo Serial char on Serial1...
    c = Serial.read()
    if c==27: break # <ESC> ?
    if c!=-1: # valid char ?
        Serial1.write(c)

    # echo Serial1 char on Serial...
    c1 = Serial1.read()
    if c1==27: break # <ESC> ?
    if c1!=-1: # valid char ?
        Serial.write(c1)

    delay(10)

Serial1.end()
Serial.end()

