
# SD
# ==

from Arduino_defines import *

# ===================

if implementation=="cpython":
    from PythonSD import *
    SDClass = PythonSDClass
    del PythonSDClass
else:
    from MicropythonSD import *
    SDClass = MicropythonSDClass
    del MicropythonSDClass

SD = SDClass()
