
# MicropythonWire
# ===============

from Arduino import *

import machine

from TwoWire import *

class MicropythonWire(TwoWire):

    def __init__(self, scl=35, sda=33): # Micropython pin's order !
        super(MicropythonWire, self).__init__()
        self._scl = scl
        self._sda = sda
        self._i2c = machine.SoftI2C(scl=machine.Pin(self._scl), sda=machine.Pin(self._sda), freq=100000, timeout=50000)
    #def __init__(self, sda=WIRE_SDA_PIN, scl=WIRE_SCL_PIN): # Arduino pin's order !
    #    super(MicropythonWire, self).__init__()
    #    self._sda = sda
    #    self._scl = scl
    #    self._i2c = machine.SoftI2C(scl=machine.Pin(self._scl), sda=machine.Pin(self._sda), freq=100000, timeout=50000)

    def __del__(self):
        del self._i2c
        super(MicropythonWire, self).__del__()

    def scl(self):
        return self._scl

    def sda(self):
        return self._sda

    def i2c(self):
        return self._i2c

    #def __bool__(self):
    #    return self._errored

    #def begin(self):
    #    pass

    #def end(self):
    #    pass

    #def beginTransmission(self, address):
    #    ## indicate that we are transmitting
    #    #transmitting = 1
    #
    #    # set address of targeted slave
    #    self._wr_address = address
    #
    #    # reset tx buffer iterator vars
    #    #_wr_index = 0
    #    self._wr_length = 0

    def endTransmission(self, sendStop=True):
        try:
            self._i2c.writeto(self._wr_address, bytes(self._wr_buffer[0:self._wr_length]), sendStop)
        except:
            return 1
        return 0

    #def write_char(self, c):
    #    self._wr_buffer[self._wr_length] = c
    #    self._wr_length += 1
    #    return 1

    def requestFrom(self, address, quantity, iaddress=0, isize=0, sendStop=True):
        self._rd_buffer = bytes(0)
        self._rd_index = 0
        try:
            bstr = bytes([iaddress>>(x*8) & 0xFF for x in range(isize-1,-1,-1)])
            self._i2c.writeto(address, bstr, False)
            self._rd_buffer = self._i2c.readfrom(address, quantity)
            return len(self._rd_buffer)
        except:
            return 0

    #def read_char(self):
    #    if self._rd_index>=len(self._rd_buffer):
    #        return -1
    #    else:
    #        c = self._rd_buffer[self._rd_index]
    #        self._rd_index += 1
    #        return c
