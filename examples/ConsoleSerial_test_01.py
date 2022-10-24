#!/usr/bin/python3

from Arduino import *

# ===================

from Stream import *

class Test(Stream):

    def __init__(self, stream):
        self._stream = stream

    def write_char(self, c):
        return self._stream.write_char(c + 1)

    def println(self, v=b''):
        return (self.print(v) + self._stream.println())

Serial.begin()

test = Test(Serial)
test.println("hello") # print to console 'ifmmp'
test.println(1234) # print to console '2345'

Serial.end()
