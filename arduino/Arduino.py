
# Arduino
# =======

from Arduino_defines import *

# ===================

if implementation=='cpython':
    if os.path.exists('Arduino_config.py'):
        from Arduino_config import *
elif implementation=='micropython':
    try:
        if bool(os.stat('Arduino_config.py')):
            from Arduino_config import *
    except:
        pass
else:
    pass

# ===================

from ConsoleSerial import *

Serial = ConsoleSerial()

#Serial.begin()
