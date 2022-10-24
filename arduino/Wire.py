from Arduino import *

if sys.implementation.name=="micropython":
    from MicropythonWire import *
    Wire = MicropythonWire(35, 33) #scl, sda
else:
    from PythonWire import *
    Wire = PythonWire(1) #num
