from Arduino import *

if implementation=="cpython":
    from PythonWire import *
    Wire = PythonWire(WIRE_I2C_NUM) #num
elif implementation=="micropython":
    from MicropythonWire import *
    Wire = MicropythonWire(WIRE_SCL_PIN, WIRE_SDA_PIN) # Micropython pin's order !
    #Wire = MicropythonWire(WIRE_SDA_PIN, WIRE_SCL_PIN) # Arduino pin's order !
else:
    pass