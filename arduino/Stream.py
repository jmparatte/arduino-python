
# Arduino class Stream
# ===================

from Print import *

class Stream(Print):

    def __init__(self):
        #print("Stream.10")
        super(Stream, self).__init__()
        self._peek = -1

    def __del__(self):
        #print("Stream.15")
        super(Stream, self).__del__()

    def read_char(self):
        return -1

    def peek(self):
        if self._peek>=0: return self._peek
        self._peek = self.read_char()
        return self._peek

    def available(self):
        if self._peek==-1: self.peek()
        if self._peek>=0:
            return 1
        else:
            return 0

    def read(self):
        c = self.peek()
        self._peek = -1
        return c
