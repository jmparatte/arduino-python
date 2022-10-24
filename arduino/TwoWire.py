
# TwoWire
# ==========

from Arduino import *

# https://www.pololu.com/file/0J435/UM10204.pdf
# https://www.nxp.com/docs/en/application-note/AN10216.pdf
# https://training.ti.com/sites/default/files/docs/adcs-i2c-introduction-the-protocol-presentation.pdf

## https://espace.cern.ch/CMS-MPA/SiteAssets/SitePages/Documents/I2C_bus_specifications_V2_0.pdf
## 4.2 AC Electrical Characteristics

# #include "Wire/src/Wire.h"
# C:\Arduino15\hardware\arduino\avr\libraries\Wire\src\Wire.h

TW_READ = 1
TW_WRITE = 0

BUFFER_LENGTH = 32
WIRE_HAS_END = 1

# #include "Wire/src/utility/twi.h"
# C:\Arduino15\hardware\arduino\avr\libraries\Wire\src\utility\twi.h

TWI_FREQ = 100000
TWI_BUFFER_LENGTH = 32

from Stream import *

class TwoWire(Stream):

    def __init__(self):
        super(TwoWire, self).__init__()
        self._errored = False
        self._wr_address = -1
        self._wr_buffer = bytearray(TWI_BUFFER_LENGTH)
        self._wr_length = 0
        self._rd_buffer = b'' #bytes(0) #bytearray(0)
        self._rd_index = 0

    def __del__(self):
        super(TwoWire, self).__del__()

    def __bool__(self):
        return self._errored

    def begin(self):
        pass

    def end(self):
        pass

    def beginTransmission(self, address):
        self._wr_address = address
        self._wr_length = 0

    def endTransmission(self, sendStop=True):
        self._wr_length = 0
        return 0

    def write_char(self, c):
        self._wr_buffer[self._wr_length] = c
        self._wr_length += 1
        return 1

    def requestFrom(self, address, quantity, iaddress=0, isize=0, sendStop=True):
        self._rd_buffer = bytes(0)
        self._rd_index = 0
        return 0 #len(self._rd_buffer)

    def read_char(self):
        if self._rd_index>=len(self._rd_buffer):
            return -1
        else:
            c = self._rd_buffer[self._rd_index]
            self._rd_index += 1
            return c

