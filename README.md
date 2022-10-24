# Arduino-Python
Arduino-Python is a Python 3 implementation of Arduino libraries and toolkit for various platforms.

The main goal of this development is to offer a quick way to migrate pure Arduino C++ libraries and programs to Python.


## Hello World!

Arduino program [HelloWorld.ino]:  
```C++
void setup() {
    Serial.begin();
    Serial.println("Hello World!");
    Serial.end();
}

void loop() {
}
```

can be translated to explicit Arduino-Python [HelloWorld-explicit.py] including translation of Arduino C++ main() function:
```python
from Arduino import *

def setup():
    Serial.begin()
    Serial.println("Hello World!")
    Serial.end()

def loop():
    pass

def main():
    setup()
    while True:
        loop()

main()
```

or can be translated to minimal shortest compact Arduino-Python [HelloWorld-compact.py] exluding unnecessary code:
```python
from Arduino import *

Serial.begin()
Serial.println("Hello World!")
Serial.end()
```


## Supported platforms

| hardware | OS          | `implementation` | `platform` | Arduino architecture |
|----------|-------------|------------------|------------|----------------------|
| PC       | Windows     | `"cpython"`      | `"win32"`  | `ARDUINO_ARCH_WIN32` |
| PC       | Mac OS      | `"cpython"`      | `"macos"`  | `ARDUINO_ARCH_MACOS` |
| PC       | Linux       | `"cpython"`      | `"linux"`  | `ARDUINO_ARCH_LINUX` |
| RPi      | RPi OS      | `"cpython"`      | `"rpios"`  | `ARDUINO_ARCH_RPIOS` |
| ESP32    | MicroPython | `"micropython"`  | `"esp32"`  | `ARDUINO_ARCH_ESP32` |

- PC/Windows is any running recent [Python] or [Thonny].
- PC/Mac OS is any running recent [Python] or [Thonny].
- PC/Linux is any running recent [Python] or [Thonny].
- RPi/RPi OS is any running recent [Python] or [Thonny].
- ESP32/MicroPython is any of ESP32, EPS32-S2 or ESP32-C3 flashed with recent [MicroPython].

- `implementation` is a Arduino-Python constant loaded before start of application. This constant is a shortcut to ```sys.implementation.name```. Its value is `"cpython"` or `"micropython"`. `implementation` can be checked with code like that:
```Python
if implementation=="micropython":
    # execute next code only if MicroPython implementation...
```
- `platform` is a Arduino-Python constant loaded before start of application. Its value is derivated from ```sys.platform``` and other checks. `platform` can be checked with code like that:
```Python
if platform=="esp32":
    # execute next code only if ESP32 hardware...
```
- `ARDUINO_ARCH_xxxxx` are Arduino-Python constants loaded before start of application. They values are all `False` but only one is `True`. They can be checked with codes like that:
```Python
if ARDUINO_ARC_ESP32:
    # execute next code only if ESP32 hardware...
```


## Arduino translated headers, classes and objects

| type    | name             | platform  | details implementation |
|---------|------------------|-----------|------------------------|
| header  | `Arduino`        | `"win32"` | digital and analog unavailable |
|         |                  | `"macos"` | digital and analog unavailable |
|         |                  | `"linux"` | digital and analog unavailable |
|         |                  | `"rpios"` | digital soon available, analog unavailable |
|         |                  | `"esp32"` | digital and analog soon available |
| class   | `Print`          | all       | full |
| class   | `Stream`         | all       | full |
| class   | `HardwareSerial` | all       | full |
| object  | `Serial`         | `"win32"` | full but restrictions by Thonny on reading |
|         |                  | `"macos"` | full but restrictions by Thonny on reading |
|         |                  | `"linux"` | full but restrictions by Thonny on reading |
|         |                  | `"rpios"` | full but restrictions by Thonny on reading |
|         |                  | `"esp32"` | full but restrictions by Thonny on reading |
| object  | `Serial1`        | `"rpios"` | full on `/dev/ttyAMA0` (UART0 TXD=8 RXD=10) |
|         |                  | `"esp32"` | full on UART1 |
|         | `Serial1`..      | `"win32"` | full on USB comport user declared |
|         |                  | `"macos"` | full on USB comport user declared |
|         |                  | `"linux"` | full on USB comport user declared |
|         |                  | `"rpios"` | full on USB comport user declared |
| class   | `TwoWire`        | all       | full |
| object  | `Wire`           | `"win32"` | I2C Restart currently unavailable |
|         |                  | `"macos"` | I2C Restart currently unavailable |
|         |                  | `"linux"` | I2C Restart currently unavailable |
|         |                  | `"rpios"` | I2C Restart currently unavailable |
|         |                  | `"esp32"` | full, soon available |
| class   | `SDClass`        | all       | soon available |
| object  | `SD`             | all       | soon available |
| class   | `File`           | all       | soon available |
| library | `jm_PCF8574`     | all       | full |
| library | `jm_LCM2004A_I2C` | all      | full |


## Serial.write(), Serial.print()

`Serial`is the Arduino console input/output. This object is implemented on a serial uart, a serial usb or a virtual serial. No restrictions apply to writing.

`Serial.write()` accepts 1 argument with 3 different meanings:  
- `c`, a 8-bit positiv integer written as single byte. This could be a character ordinal value or a data byte. Exemple: `Serial.write(ord('A')) # write byte 65`
- `bstr`, a Python bytes object written as bytes. Exemple: `Serial.write(b'hello\r\n') # write 7 bytes`
- `str`, a Python unicode string converted to utf-8 bytes and then written. Exemple: `Serial.write('é') # write 2 bytes b'\xc3\xa9'`

`Serial.print()` accepts 1 argument with 3 different meanings:  
- `n`, a Python number printed as a human-readable string. Exemple: `Serial.print(65) # write bytes b'65'`
- `bstr`, same behaviour as 'Serial.write()`
- `str`, same behaviour as 'Serial.write()`

`Serial.write()` and `Serial.print()` returns the number of written bytes.

`Serial.println()` proceeds same as `Serial.print()` but append `b'\r\n'` end-of-line.

`Serial1` and next have the same methods than `Serial`.


## Serial.read()

`Serial`is the Arduino console input/output. This object is implemented on a serial uart, a serial usb or a virtual serial. Restrictions apply to reading.

`Serial.read()` has no argument, it returns either of:  
- integer value -1 if no data is available
- a 8-bit positiv integer representing a character ordinal value or a data byte. The character ordinal value can be converted to str with `chr()` function. Example 1: `str += chr(65) # append 'A' to str`. Exemple 2: `bstr += chr(65).encode() # append b'A' to bstr`

Restrictions are of 2 types:
- programs running with [thonny] can't have a true byte per byte reading. On 1st `Serial.read()`, a full input line is read, buffered and ended with `<CR><LF>`, and then read byte per byte. Waiting the input line, the program is stopped, control is not give back until a ending line is typed!
- in practice, read characters is limited to ascii charset excluding control characters and `<DEL>` character. A 8-bit encoder/decoder to/from ascii charset must be implemented to exchange unrestricted data via the console.

`Serial1` and next have the same methods than `Serial` but without restrictions.


## Folders contents

- [arduino] - Arduino core translated to Python
- [libraries] - Arduino libraries translated to Python
- [examples] - Arduino-Python examples
- [cgi-bin] - Python CGI scripts for HTTP Web servers
- [tools] - Python tools

Additional informations are given in each folders.

## Basic usage

- Create a `<arduino-python>` development folder.
- Copy all [arduino] files into the `<arduino-python>` development folder.
- Copy other files to learn from [libraries] and [examples] into the `<arduino-python>` development folder.
- Executing from _Windows Command_, type `python <scriptname>` or simply `<scriptname>` (verify that `Python` is correctly written in `PATH` environment).
- Executing from _Linux Terminal_, type `python <scriptname>` or simply `./<scriptname>` (don't forget to set _executable permissions_ to `<scriptname>`, look at [How to run a Python script in Linux] for howto).
- Executing from [Thonny] - _Python IDE for beginners_, load `<scriptname>` and run it.
- Enjoy :smiley:

[arduino]: <arduino>
[libraries]: <libraries>
[examples]: <examples>
[cgi-bin]: <cgi-bin>
[tools]: <tools>

[HelloWorld.ino]: <examples/HelloWorld.ino>
[HelloWorld-explicit.py]: <examples/HelloWorld-explicit.py>
[HelloWorld-compact.py]: <examples/HelloWorld-compact.py>

[jm_LCM2004A_I2C_charset.py]: <examples/jm_LCM2004A_I2C_charset.py>
[jm_LCM2004A_I2C_demo1.ino]: <https://github.com/jmparatte/jm_LCM2004A_I2C/blob/master/examples/jm_LCM2004A_I2C_demo1/jm_LCM2004A_I2C_demo1.ino>

[Arduino]: <https://www.arduino.cc/>
[Python]: <https://www.python.org/>
[Thonny]: <https://thonny.org/>
[MicroPython]: <https://micropython.org/>

[How to run a Python script in Linux]: <https://www.educative.io/answers/how-to-run-a-python-script-in-linux>

[//]: # (
Look at [jm_LCM2004A_I2C_charset.py] example translated from [jm_LCM2004A_I2C_demo1.ino] Arduino example.
Python implementation of Arduino libraries and toolkit for Windows and Linux platforms, and also for MicroPython ESP32
https://www.markdownguide.org/
https://dillinger.io/
)
