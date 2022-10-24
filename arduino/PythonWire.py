
# PythonWire
# ==========

from Arduino import *

#import smbus
import smbus2

from TwoWire import *

class PythonWire(TwoWire):

    def __init__(self, num=1):
        super(PythonWire, self).__init__()
        self._num = num
        self._smbus2 = smbus2.SMBus(self._num)

    def __del__(self):
        del self._smbus2
        super(PythonWire, self).__del__()

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
        if sendStop==False: raise NameError("Option 'sendStop==False' currently not implemented!")
        try:
            msg = smbus2.i2c_msg.write(self._wr_address, [x for x in self._wr_buffer[0:self._wr_length]])
            self._smbus2.i2c_rdwr(msg)
            self._wr_length = 0
        except:
            return 1
        return 0

    #def write_char(self, c):
    #    self._wr_buffer[self._wr_length] = c
    #    self._wr_length += 1
    #    return 1

    def requestFrom(self, address, quantity, iaddress=0, isize=0, sendStop=True):
        if sendStop==False: raise NameError("Option 'sendStop==False' currently not implemented!")
        self._rd_buffer = bytes(0)
        self._rd_index = 0
        msgs = []
        if isize>0:
            msgs.append( smbus2.i2c_msg.write(address, [iaddress>>(x*8) & 0xFF for x in range(isize-1,-1,-1)]) )
        msgs.append( smbus2.i2c_msg.read(address, quantity) )#, quantity) )
        self._smbus2.i2c_rdwr(*msgs)
        for msg in msgs:
            if msg.flags==1:
                self._rd_buffer += bytes([int(x) for x in msg.__bytes__()])
        return len(self._rd_buffer)

    #def read_char(self):
    #    if self._rd_index>=len(self._rd_buffer):
    #        return -1
    #    else:
    #        c = self._rd_buffer[self._rd_index]
    #        self._rd_index += 1
    #        return c
