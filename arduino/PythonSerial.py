
# Arduino class PythonSerial
# ==========================

from Arduino_defines import *
from HardwareSerial import *

import serial

class PythonSerial(HardwareSerial):

    def __init__(self, comm_port):

        HardwareSerial.__init__(self)

        self._comm_port = comm_port

        self._uart = None #serial.Serial() #None

    def begin(self, baudrate=9600, settings=SERIAL_8N1): # return OK

        if not HardwareSerial.begin(self, baudrate, settings): return False

        self._uart = serial.Serial(port=self._comm_port, \
                                   baudrate=self._baudrate, \
                                   bytesize=self._bits, parity=self._settings[1], stopbits=self._stop, \
                                   timeout=0, xonxoff=False, rtscts=False, write_timeout=None, \
                                   dsrdtr=False, inter_byte_timeout=None, exclusive=None)

        self._connected = self._uart != None

        return self._connected

    def end(self): # return OK

        if not self._connected: return False

        self._uart.close()
        self._uart = None #serial.Serial() #None
        self._connected = False

        return HardwareSerial.end(self)
