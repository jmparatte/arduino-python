
# Arduino class HardwareSerial
# ============================

from Arduino_defines import *

# https://www.arduino.cc/reference/en/language/functions/communication/serial/

SERIAL_5N1 = "5N1"
SERIAL_6N1 = "6N1"
SERIAL_7N1 = "7N1"
SERIAL_8N1 = "8N1"
SERIAL_5N2 = "5N2"
SERIAL_6N2 = "6N2"
SERIAL_7N2 = "7N2"
SERIAL_8N2 = "8N2"
SERIAL_5E1 = "5E1"
SERIAL_6E1 = "6E1"
SERIAL_7E1 = "7E1"
SERIAL_8E1 = "8E1"
SERIAL_5E2 = "5E2"
SERIAL_6E2 = "6E2"
SERIAL_7E2 = "7E2"
SERIAL_8E2 = "8E2"
SERIAL_5O1 = "5O1"
SERIAL_6O1 = "6O1"
SERIAL_7O1 = "7O1"
SERIAL_8O1 = "8O1"
SERIAL_5O2 = "5O2"
SERIAL_6O2 = "6O2"
SERIAL_7O2 = "7O2"
SERIAL_8O2 = "8O2"

from Stream import *

class HardwareSerial(Stream):

    def __init__(self):

        super(HardwareSerial, self).__init__()

        self._baudrate = 0
        self._baudrate_us = 0
        self._settings = ""
        self._bits = 0
        self._parity = 0
        self._stop = 0
        self._char_bits = 0
        self._char_us = 0
        self._char_ms = 0

        self._connected = False
        self._uart = None

    def __del__(self):
        self.end()
        super(HardwareSerial, self).__del__()

    def __bool__(self):
        return self._connected

    def connected(self):
        return self._connected

    def uart(self):
        return self._uart

    def begin(self, baudrate=9600, settings=SERIAL_8N1): # return OK

        if self._connected: return False

        self._baudrate = baudrate
        self._baudrate_us = (1000000 + self._baudrate -1) // self._baudrate #ceil
        self._settings = settings
        #print(self._baudrate, self._baudrate_us, self._settings)

        self._bits = (ord(self._settings[0]) - ord('0'))
        self._parity = (0 if self._settings[1]=='E' else (1 if self._settings[1]=='O' else None))
        self._stop = (2 if self._settings[2]=='2' else 1)
        #print(self._bits, self._parity, self._stop)

        self._char_bits = (1 + self._bits + (1 if self._parity!=None else 0) + self._stop)
        self._char_us = (self._char_bits*1000000 + self._baudrate - 1) // self._baudrate #ceil
        self._char_ms = (self._char_us + 1000 - 1) // 1000 #ceil
        #print(self._char_bits, self._char_us, self._char_ms)

        #self._connected = self._uart != None

        return True #return self._connected

    def end(self): # return OK

        if self._connected: return False

        #self._connected = False

        return True

    def read_char(self):
        if not self._connected: return -1
        c = self._uart.read(1)
        c = -1 if (c==None or c==b'') else c[0]
        return c

    def write_char(self, c):
        if not self._connected: return 0
        return self._uart.write(bytes((c,)))
