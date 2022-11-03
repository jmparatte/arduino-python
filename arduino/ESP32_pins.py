
# ESP32_pins
# ==========

from Arduino import *

from machine import Pin
from machine import ADC

# Arduino digital modes:
# ---------------------
#INPUT  = 0x0
#OUTPUT = 0x1
#INPUT_PULLUP = 0x2
#OUTPUT_OPENC = 0x3 # extra Open Collector

# Extended pin's modes:
# --------------------
PIN_ADC     = -2    # Analog Digital Conversion
PIN_NONE    = -1    # no pin, pin not connected
PIN_INPUT   = 0     # same as Arduino INPUT
PIN_OUTPUT  = 1     # same as Arduino OUTPUT
PIN_INPUT_PULLUP = 2 # same as Arduino INPUT_PULLUP
PIN_OUTPUT_OPENC = 3 # same as Arduino OUTPUT_OPENC

_pins: [(int, Pin, ADC), ...] = [None]*41 # LOLIN S2 mini - ESP32-S2: gpio0...gpio40

def pinMode(pin, mode=None):
    if mode==None:
        if pin==-1: return PIN_NONE
        if _pins[pin]==None: return PIN_NONE
        return _pins[pin][0] # mode
    if pin==-1: return
    if mode==INPUT:
        _pins[pin] = (mode, Pin(pin, Pin.IN), None)
    elif mode==OUTPUT:
        _pins[pin] = (mode, Pin(pin, Pin.OUT, value=0), None)
    elif mode==INPUT_PULLUP:
        _pins[pin] = (mode, Pin(pin, Pin.IN, Pin.PULL_UP), None)
    elif mode==OUTPUT_OPENC:
#        _pins[pin] = (mode, Pin(pin, Pin.OPEN_DRAIN, Pin.PULL_UP, value=1), None)
        _pins[pin] = (mode, Pin(pin, Pin.OPEN_DRAIN, value=1), None)
    else:
        _pins[pin] = None

def digitalWrite(pin, value):
    if pin==-1: return
    _pins[pin][1].value(value)

def digitalRead(pin):
    if pin==-1: return LOW
    return _pins[pin][1].value()

#pinMode(LED_BUILTIN, INPUT)
pinMode(LED_BUILTIN, OUTPUT)
#pinMode(LED_BUILTIN, INPUT_PULLUP)
#pinMode(LED_BUILTIN, OUTPUT_OPENC)
print(repr(_pins))
for _ in range(1):
    digitalWrite(LED_BUILTIN, HIGH)
    print(digitalRead(LED_BUILTIN))
    delay(100)
    digitalWrite(LED_BUILTIN, LOW)
    print(digitalRead(LED_BUILTIN))
    delay(100)

pinMode(LED_BUILTIN, -1)
print(repr(_pins))

# analog pins: 1...10

def analogRead(pin):
    if pin==-1: return 0
    if _pins[pin]==None or _pins[pin][0]!=PIN_ADC:
        _pins[pin] = (PIN_ADC, None, ADC(Pin(pin)))
    return _pins[pin][2].read()

for _ in range(10):
    print(analogRead(7))

print(repr(_pins))

pinMode(0, INPUT_PULLUP)
for _ in range(100):
    print(digitalRead(0))
    delay(100)
    