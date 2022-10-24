
# Arduino defines
# ===============

import sys
import time #as time
import os

implementation = sys.implementation.name # "cpython" or "micropython" (other implementations not checked)

python_detected = implementation=="cpython"
micropython_detected = implementation=="micropython"

try:
    #thonny_detected = bool(globals()['__thonny_helper']) # True if exists and non-empty
    #thonny_detected = bool(globals()['_thonny_repl_print']) # True if exists and non-empty
    if python_detected:
        thonny_detected = bool(os.environ['THONNY_USER_DIR']) # True if exists and non-empty
    elif micropython_detected:
        thonny_detected = time.time()>31*86400 # > 1 month from hardware reset
        # WARNING: false detection if time modified by program using machine.RTC()
    else:
        thonny_detected = False
except:
    thonny_detected = False

platform = sys.platform # "win32" or "darwin" or "linux" or "esp32" (other platforms not checked with Arduino-Python)

if platform=="linux":
    try:
        rpi_model = open("/sys/firmware/devicetree/base/model").read()[:-1]
        # 'Raspberry Pi 3 Model B Plus Rev 1.3'
        if rpi_model.startswith('Raspberry Pi'):
            platform = "rpios"
    except:
        rpi_model = None

# Python architectures:
ARDUINO_ARCH_WIN32 = platform=="win32"
ARDUINO_ARCH_MACOS = platform=="darwin"
ARDUINO_ARCH_LINUX = platform=="linux"
ARDUINO_ARCH_RPIOS = platform=="rpios"
# Micropython architectures:
ARDUINO_ARCH_ESP32 = platform=="esp32"

# ordinal value of some ASCII chars...
CHR_NUL = 0x00
CHR_STX = 0x02
CHR_ETX = 0x03
CHR_ACK = 0x06
CHR_TAB = 0x09 # ord('\t')
CHR_LF  = 0x0A # ord('\n')
CHR_CR  = 0x0D # ord('\r')
CHR_NAK = 0x15
CHR_ESC = 0x1B
CHR_SP  = 0x20 # ord(' ')
CHR_DEL = 0x7F

STR_CRLF = "\r\n"
BSTR_CRLF = b"\r\n" # "\r\n".encode() # bytes((0x0D,0x0A))

STR_BOM = "\uFEFF" # BOM UTF-8 https://en.wikipedia.org/wiki/Byte_order_mark
BSTR_BOM = b"\xEF\xBB\xBF" # "\uFEFF".encode() # "".encode("utf-8-sig")

HIGH = 0x1
LOW  = 0x0

INPUT  = 0x0
OUTPUT = 0x1
INPUT_PULLUP = 0x2
OUTPUT_OPENC = 0x3 # extra Open Collector
INPUT_PULLDN = 0x4 # extra Pull-down

PI = 3.1415926535897932384626433832795
HALF_PI = 1.5707963267948966192313216916398
TWO_PI = 6.283185307179586476925286766559
DEG_TO_RAD = 0.017453292519943295769236907684886
RAD_TO_DEG = 57.295779513082320876798154814105
EULER = 2.718281828459045235360287471352

SERIAL  = 0x0
DISPLAY = 0x1

LSBFIRST = 0
MSBFIRST = 1

min = lambda a, b: (a if a<b else b)

max = lambda a, b: (a if a>b else b)

abs = lambda x: (x if x>0 else -x)

def millis():
    return time.time_ns()//1000000

def micros():
    return time.time_ns()//1000

def delay(ms):
    time.sleep(ms/1000)

def delayMicroseconds(us):
    time.sleep(us/1000000)

OK = True
ER = False

_OK_ = b"_OK_"
_ER_ = b"#ER#"

false = False
true = True
