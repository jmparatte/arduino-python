
# Arduino class ConsoleSerial
# ===========================

# https://github.com/joeyespo/py-getch/blob/master/getch/getch.py

from Arduino_defines import *
from HardwareSerial import *

if thonny_detected:
    global thonny_input_str, thonny_input_idx
    thonny_input_str, thonny_input_idx = ('', 0)
else:
    if ARDUINO_ARCH_WIN32:
        import msvcrt
        #msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    else:
        import sys
        import select

class ConsoleSerial(HardwareSerial):

    def __init__(self):
        super(ConsoleSerial, self).__init__()

    def __del__(self):
        self.end()
        super(ConsoleSerial, self).__del__()

    def begin(self, baudrate=9600, settings=SERIAL_8N1): # return OK
        if not HardwareSerial.begin(self, baudrate, settings): return False
        self._connected = True
        return self._connected

    def end(self): # return OK
        if not self._connected: return False
        self._connected = False
        return HardwareSerial.end(self)

    def write_char(self, c):
        return self.write_bstr(bytes((c,)))

    def write_bstr(self, b):
        if not self._connected: return 0
        if python_detected:
            print(b.decode(), end='', flush=True)
        else:
            print(b.decode(), end='')
        return len(b)

    def write_str(self, s):
        if not self._connected: return 0
        if python_detected:
            print(s, end='', flush=True)
        else:
            print(s, end='')
        return len(s.encode())

    def read_char(self):
        if not self._connected: return -1
        if thonny_detected:
            global thonny_input_str, thonny_input_idx
            if len(thonny_input_str)==thonny_input_idx: # end of buffer ?
                thonny_input_str, thonny_input_idx = (input() + STR_CRLF, 0)
            c = ord(thonny_input_str[thonny_input_idx])
            thonny_input_idx += 1
        else:
            if ARDUINO_ARCH_WIN32:
                if msvcrt.kbhit():
                    c = ord(msvcrt.getch())
                else:
                    c = -1
            else:
                list = select.select([sys.stdin], [], [], 0)
                if list[0]:
                    c = ord(sys.stdin.read(1))
                else:
                    c = -1
        return c