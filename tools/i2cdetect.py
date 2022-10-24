#!/usr/bin/python3

# https://www.kernel.org/doc/Documentation/i2c/i2c-protocol
# https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
# https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all
# http://wiki.erazor-zone.de/wiki:linux:python:smbus:doc
# https://github.com/kplindegaard/smbus2/blob/master/smbus2/smbus2.py
# https://pypi.org/project/smbus2/
# https://smbus2.readthedocs.io/en/latest/

# https://forums.raspberrypi.com/viewtopic.php?t=114401

# man i2cdetect

"""
pi@raspberrypi:~ $ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- 27 -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
"""

import smbus2
import errno

def i2cdetect():
    bus_number = 1  # 1 indicates /dev/i2c-1
    bus = smbus2.SMBus(bus_number)
    device_count = 0

    for device in range(0x00, 128):
        if device==0:
            print("   ", " 0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f", end="")
        if device%16==0:
            print()
            print("{0:02x}:".format(device), end="")
        if device<0x08 or device>0x77:
            print("", "  ", end="")
        else:
            try:
                msg = smbus2.i2c_msg.write(device, [])
                bus.i2c_rdwr(msg)
                print("", "{0:2x}".format(device), end="")
                device_count = device_count + 1
            except IOError as e:
                if e.errno == errno.EREMOTEIO:
                    print("", "--", end="")
                else:
                    print("", "!!", end="")
            except Exception as e:
                print("", "##", end="")
    print()

    bus.close()
    bus = None

    print("Found {0} device(s)".format(device_count))

if __name__ == "__main__":
    i2cdetect()
