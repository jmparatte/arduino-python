#!/usr/bin/python3

from Arduino import *

# ===================

if ARDUINO_ARCH_WIN32:
    from PythonSerial import *
    #Serial1 = PythonSerial("COM1") # FTDI/Win32
    Serial1 = PythonSerial("COM91") # FTDI/Win32
elif ARDUINO_ARCH_MACOS:
    from PythonSerial import *
    Serial1 = PythonSerial("/dev/ttyUSB0") # FTDI/Linux
elif ARDUINO_ARCH_LINUX:
    from PythonSerial import *
    Serial1 = PythonSerial("/dev/ttyUSB0") # FTDI/Linux
elif ARDUINO_ARCH_RPIOS:
    from PythonSerial import *
    Serial1 = PythonSerial("/dev/ttyUSB0") # FTDI/Linux
elif ARDUINO_ARCH_ESP32:
    from MicropythonSerial import *
    #Serial1 = MicropythonSerial(1, 10, 9) # ESP32-S2 serial_num=1 tx_pin=10 rx_pin=9
    Serial1 = MicropythonSerial(1, 3, 5) # ESP32-S2 serial_num=1 tx_pin=3 rx_pin=5
else:
    pass

# ===================

Serial.begin(115200)
Serial1.begin(115200)

while True:
    c1 = Serial1.read()
    if c1==27:
        break # <ESC> ?
    if c1!=-1:
        Serial.write(c1)

    c2 = Serial.read()
    if c2==27:
        break # <ESC> ?
    if c2!=-1:
        Serial1.write(c2)

    delay(1)

Serial1.end()
Serial.end()

