
# Arduino class MicroPythonSerial
# ===============================

from Arduino_defines import *
from HardwareSerial import *

from machine import UART

class MicropythonSerial(HardwareSerial):

    def __init__(self, num, tx, rx):

        HardwareSerial.__init__(self)

        self._num = num
        self._tx = tx
        self._rx = rx

        self._uart = UART(self._num, tx=self._tx, rx=self._rx)

    def begin(self, baudrate=9600, settings=SERIAL_8N1): # return OK

        if not HardwareSerial.begin(self, baudrate, settings): return False

        #self._uart = UART(self._num, tx=self._tx, rx=self._rx, \
        self._uart = UART(self._num, \
        #self._uart.init( \
                          tx=self._tx, rx=self._rx, \
                          baudrate=self._baudrate, \
                          bits=self._bits, parity=self._parity, stop=self._stop, \
                          timeout=0, timeout_char=0, \
                          invert=0, \
                          flow=0)

        self._connected = self._uart != None

        return self._connected

    def end(self): # return OK

        if not self._connected: return False

        #self._uart.deinit() ##do not deinit esp32 UART!!! #
        #self._uart = None
        self._connected = False

        return HardwareSerial.end(self)
