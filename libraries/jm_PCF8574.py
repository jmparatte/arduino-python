from Arduino import *
from Wire import *

# ------------------------------------------------------------------------------

# PCF8574 - PCF8574A
# Remote 8-bit I/O expander for I2C-bus with interrupt

# http://www.ti.com/lit/ml/scyb031/scyb031.pdf
# http://www.ti.com/lit/ds/symlink/pcf8574.pdf
# https://www.nxp.com/docs/en/data-sheet/PCF8574_PCF8574A.pdf

# PCF8574 I2C address: 0x20..0x27
# PCF8574A I2C address: 0x38..0x3F

# Quasi-bidirectional I/Os: P0..P7

# ------------------------------------------------------------------------------

from Stream import *

class jm_PCF8574(Stream):

    def __init__(self, i2c_address=0, wire=Wire):
        super(jm_PCF8574, self).__init__()
        self._i2c_address = i2c_address # set device I2C address
        self._wire = wire
        self._connected = False         # set device not connected (disconnected)
        self._io_mask = 0x00            # set digital I/O mask P0-P7 as INPUT
        self._io_data = 0xFF            # set digital I/O data P0-P7 as INPUT

    def __del__(self):
        self.end()
        super(jm_PCF8574, self).__del__()

    def __bool__(self):
        return self._connected

    def i2c_address(self):
        return self._i2c_address

    def wire(self):
        return self._wire

    def connected(self):
        return self._connected

# ------------------------------------------------------------------------------

    def _begin(self): # return OK
        if (self._connected): return True # allready connected ? OK

        if (self._i2c_address == 0x00): return False # I2C address not set ? !OK

        self._connected = True

        # check access to device...

        self._wire.beginTransmission(self._i2c_address) # check access device
        self._connected = (self._wire.endTransmission() == 0) # I2C device acknowledge ? OK

        return self._connected

    def begin(self, i2c_address=0): # return OK
        if (i2c_address != 0):
            if (self._connected and self._i2c_address != i2c_address): return False # allready connected on another address ? !OK
            self._i2c_address = i2c_address
        return self._begin()

    def end(self):
        self._connected = False
        return True

# ------------------------------------------------------------------------------

    def read_char(self):
        if (not self._connected):
            return -1
        if (self._wire.requestFrom(self._i2c_address, 1) != 1):
            self._connected = False
            return -1;
        return self._wire.read();

    def write_char(self, c):
        if (not self._connected):
            return 0
        self._wire.beginTransmission(self._i2c_address)
        if (self._wire.write(c) != 1):
            self._connected = False
            return 0
        if (self._wire.endTransmission(True) != 0):
            self._connected = False
            return 0
        return 1

    def write_bstr(self, b):
        if (not self._connected):
            return 0
        self._wire.beginTransmission(self._i2c_address)
        if (self._wire.write(b) != len(b)):
            self._connected = False
            return 0
        if (self._wire.endTransmission(True) != 0):
            self._connected = False
            return 0
        return len(b)

# ------------------------------------------------------------------------------

    def pinMask(self, pin):
        return (1 << pin)

    def pinMode(self, pin, mode=None):
        if mode==None:
            if (self._io_mask & (1 << pin)):
                return OUTPUT # OPEN_DRAIN
            else:
                return INPUT # INPUT_PULLUP
        else:
            if (mode == OUTPUT):
                self._io_mask |= (1 << pin) # OPEN_DRAIN
            else:
                self._io_mask &= ~(1 << pin) # INPUT_PULLUP
            self._io_data |= ~self._io_mask # force digital pin to HIGH if configured as INPUT
            #return None

    def digitalRead(self, pin):
        result = self.read()
        if (result == -1):
            return LOW
        else:
            return (HIGH if result & (1 << pin) else LOW)

    def digitalWrite(self, pin, value):
        io_data1 = ((1 << pin) if value else 0)
        io_mask1 = (self._io_mask & (1 << pin))

        self._io_data |= (io_data1 & io_mask1) # set pin to HIGH if value is HIGH and pin is configured as OUTPUT
        self._io_data &= ~(~io_data1 & io_mask1) # set pin to LOW if value is LOW and pin is configured as OUTPUT

        self.write(self._io_data)

# ------------------------------------------------------------------------------

    def wait(self, us):
        if (us > 100): delayMicroseconds(us - 100)
        #return True
