
# Arduino
# =======

from Arduino_defines import *

# ===================

import os as _os

if implementation=='cpython':
    if _os.path.exists('Arduino_config.py'):
        from Arduino_config import *
elif implementation=='micropython':
    try:
        if bool(_os.stat('Arduino_config.py')):
            from Arduino_config import *
    except:
        pass
else:
    pass

# ===================

from ConsoleSerial import *

Serial = ConsoleSerial()

#Serial.begin()
