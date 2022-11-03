# Arduino-Python

Arduino-Python est une impl�mentation Python/MicroPython des biblioth�ques Arduino et de la bo�te � outils pour diverses plates-formes telles que Raspberry PI et ESP32.

L'objectif principal de ce d�veloppement est d'offrir un moyen rapide de migrer des biblioth�ques et des programmes Arduino C++ vers Python/MicroPython.


## Hello World!

Le programme Arduino [HelloWorld.ino]:
```C++
void setup() {
    Serial.begin();
    Serial.println("Hello World!");
    Serial.end();
}

void loop() {
}
```

peut �tre traduit en Arduino-Python explicite [HelloWorld_explicit.py], y compris la traduction de la fonction Arduino C++ `main()`:
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

ou peut �tre traduit en Arduino-Python compact plus court [HelloWorld_compact.py] en excluant le code inutile:
```python
from Arduino import *

Serial.begin()
Serial.println("Hello World!")
Serial.end()
```


## Platformes support�es

| hardware | OS          | `implementation` | `platform` | Arduino architecture |
|----------|-------------|------------------|------------|----------------------|
| PC       | Windows     | `"cpython"`      | `"win32"`  | `ARDUINO_ARCH_WIN32` |
| PC       | Mac OS      | `"cpython"`      | `"macos"`  | `ARDUINO_ARCH_MACOS` |
| PC       | Linux       | `"cpython"`      | `"linux"`  | `ARDUINO_ARCH_LINUX` |
| RPi      | RPi OS      | `"cpython"`      | `"rpios"`  | `ARDUINO_ARCH_RPIOS` |
| ESP32    | MicroPython | `"micropython"`  | `"esp32"`  | `ARDUINO_ARCH_ESP32` |

- PC/Windows est tout PC op�rant un [Python] ou [Thonny] r�cent.
- PC/Mac OS est tout Mac op�rant un [Python] ou [Thonny] r�cent.
- PC/Linux est tout Linux op�rant un [Python] ou [Thonny] r�cent.
- RPi/RPi OS est tout RPi op�rant un [Python] ou [Thonny] r�cent.
- ESP32/MicroPython est tout ESP32, EPS32-S2 ou ESP32-C3 flash� avec un [MicroPython] r�cent.

- `implementation` est une constante Arduino-Python charg�e avant le d�marrage de l'application. Cette constante est un raccourci vers `sys.implementation.name`. Sa valeur est `"cpython"` ou `"micropython"`. `implementation` peut �tre v�rifi�e avec un code comme celui-ci:
```Python
if implementation=="micropython":
    # execute next code only if MicroPython implementation...
```
- `platform` est une constante Arduino-Python charg�e avant le d�marrage de l'application. Sa valeur est d�riv�e de `sys.platform` et d'autres v�rifications. `platform` peut �tre v�rifi�e avec un code comme celui-ci:
```Python
if platform=="esp32":
    # execute next code only if ESP32 hardware...
```
- `ARDUINO_ARCH_xxxxx` sont des constantes Arduino-Python charg�es avant le d�marrage de l'application. Leurs valeurs sont toutes `False` mais une seule est `True`. Elles peuvent �tre v�rifi�s avec un code comme celui-ci:
```Python
if ARDUINO_ARCH_ESP32:
    # execute next code only if ESP32 hardware...
```


## En-t�tes, classes et objets Arduino traduits

| type    | name               | platform  | details implementation |
|---------|--------------------|-----------|------------------------|
| header  | `Arduino`          | `"win32"` | I/O, Wire, SPI unavailable |
|         |                    | `"macos"` | I/O, Wire, SPI unavailable |
|         |                    | `"linux"` | I/O, Wire, SPI unavailable |
|         |                    | `"rpios"` | digital soon available |
|         |                    | `"esp32"` | digital and analog ready, pwm soon available |
| class   | `String`           | all       | not yet implemented |
| class   | `Print`            | all       | ready, not fully implemented |
| class   | `Stream`           | all       | ready, not fully implemented |
| class   | `HardwareSerial`   | all       | full |
| object  | `Serial`           | `"win32"` | full but with Thonny's reading restrictions |
|         |                    | `"macos"` | full but with Thonny's reading restrictions |
|         |                    | `"linux"` | full but with Thonny's reading restrictions |
|         |                    | `"rpios"` | full but with Thonny's reading restrictions |
|         |                    | `"esp32"` | full but with Thonny's reading restrictions |
| object  | `Serial0`          | `"rpios"` | full on UART0 `/dev/ttyAMA0` (TXD=8 RXD=10) |
| object  | `Serial1` ...      | `"win32"` | full on USB user declared comport |
|         |                    | `"macos"` | full on USB user declared comport |
|         |                    | `"linux"` | full on USB user declared comport |
|         |                    | `"rpios"` | full on USB user declared comport |
| object  | `Serial1`          | `"esp32"` | full on UART1 (various pins) |
| class   | `TwoWire`          | all       | full |
| object  | `Wire`             | `"win32"` | unavailable |
|         |                    | `"macos"` | unavailable |
|         |                    | `"linux"` | unavailable |
|         |                    | `"rpios"` | full |
|         |                    | `"esp32"` | full |
| class   | `File`             | all       | full |
| class   | `SDClass`          | all       | full |
| object  | `SD`               | all       | full |


## Librairies Arduino-Python

| library/class                     | platform  | summary |
|-----------------------------------|-----------|---------|
| [jm_PCF8574.py]                   | all       | read/write I2C PCF8574 Quasi-bidirectional I/Os |
| [jm_LCM2004A_I2C.py]              | all       | read/write I2C Liquid Crystal Module 2004A |
| [jm_time.py]                      | all       | Python/MicroPython `time` replacement with same/standard UNIX epoch, timezone support and more |


## Exemples Arduino-Python

| example                           | platform  | summary |
|-----------------------------------|-----------|---------|
| [HelloWorld_explicit.py]          | all       | `Serial.print()` basic demo with explicit `main()` function |
| [HelloWorld_compact.py]           | all       | `Serial.print()` basic demo with compact code |
| [Serial_read_char.py]             | all       | `Serial.read()` basic demo with Thonny's reading restrictions |
| [jm_LCM2004A_I2C_HelloWorld.py]   | all       | `lcd.print()` basic demo |
| [jm_LCM2004A_I2C_PrintScreen.py]  | all       | `lcd.read()` basic demo |


## Serial.write(), Serial.print()

`Serial` est l'entr�e/sortie de la console Arduino. Cet objet est impl�ment� sur un uart s�riel, un usb s�riel ou un s�riel virtuel. Aucune restriction ne s'applique � l'�criture.

`Serial.write()` accepte 1 argument avec 3 significations diff�rentes:
- `c`, un entier positif de 8 bits �crit sur un seul octet.
Il peut s'agir de la valeur ordinale d'un caract�re ou d'un octet de donn�es.
Exemple�: `Serial.write(ord('A')) # �criture de l'octet 65`
- `bstr`, un objet Python `bytes` �crit en une s�rie d'octets.
Exemple�: `Serial.write(b'hello\r\n') # �crit 7 octets`
- `str`, une cha�ne Python unicode convertie en octets utf-8 puis �crite.
Exemple�: `Serial.write('�') # �crit 2 octets�: b'\xc3\xa9'`

`Serial.print()` accepte 1 argument avec 3 significations diff�rentes�:
- `n`, un nombre Python imprim� sous forme de cha�ne lisible par l'homme.
Exemple�: `Serial.print(65) # �crit la s�rie d'octets b'65'`
- `bstr`, m�me comportement que `Serial.write()`
- `str`, m�me comportement que `Serial.write()`

`Serial.write()` et `Serial.print()` renvoient le nombre d'octets �crits.

`Serial.println()` proc�de de la m�me mani�re que `Serial.print()` mais ajoute `b'\r\n'` en fin de ligne.

`Serial0` (Raspberry Pi), `Serial1` et suivants ont les m�mes m�thodes que `Serial`.

## Serial.read()

`Serial` est l'entr�e/sortie de la console Arduino.
Cet objet est impl�ment� sur un uart s�riel, un usb s�riel ou un s�riel virtuel.
Des restrictions s'appliquent � la lecture.

`Serial.read()` n'a pas d'argument, il renvoie soit:
- la valeur enti�re `-1` si aucune donn�e n'est disponible.
- un entier positif 8 bits repr�sentant la valeur ordinale d'un caract�re ou d'un octet de donn�es.
La valeur ordinale du caract�re peut �tre convertie en `str` par la fonction `chr()`.
Exemple 1 : `str += chr(65) # ajoute 'A' � str`.
Exemple 2�: `bstr += chr(65).encode() # ajoute b'A' � bstr`

Les restrictions sont de 2 types :
- les programmes ex�cut�s via l'IDE [Thonny] ne peuvent pas avoir une v�ritable lecture de la console caract�re par caract�re.
Lors de l'ex�cution du 1er�`Serial.read()`, une ligne d'entr�e compl�te est lue, mise en m�moire tampon et compl�t�e par `<CR><LF>`, puis lue caract�re par caract�re.
Lors de la lecture de la ligne d'entr�e, le programme est bloqu� et le contr�le n'est pas rendu tant qu'un caract�re de fin de ligne n'est pas tap�!
- en pratique, les caract�res lus par la console sont limit�s au jeu de caract�res `ascii` 7 bits � l'exclusion des caract�res de contr�le et du caract�re `<DEL>`.
Un encodeur/d�codeur 8 bits vers/depuis le jeu de caract�res `ascii` avec somme de contr�le doit �tre impl�ment� pour �changer des donn�es s�curis�es sans restriction via la console.

`Serial0` (Raspberry Pi), `Serial1` et suivants ont les m�mes m�thodes que `Serial` toutefois sans aucune restriction de lecture.

## Folders contents

- [arduino] - Core Arduino traduits en Python
- [libraries] - Librairies Arduino traduites en Python
- [examples] - Exemples Arduino-Python
- [cgi-bin] - Scripts CGI Python pour serveurs Web HTTP
- [tools] - Outils Python

Des informations compl�mentaires sont donn�es dans chaque dossier.


## Installation

- Cr�ez un dossier de d�veloppement `<arduino-python>`.
- Copiez tous les fichiers [arduino] dans le dossier de d�veloppement `<arduino-python>`.
- Copiez les autres fichiers � �tudier de [libraries] et [examples] dans le dossier de d�veloppement `<arduino-python>`.


## Usage basique

- Ouvrez le dossier de d�veloppement `<arduino-python>`.
- En ex�cutant depuis _Windows Command_, tapez `python <scriptname>` ou simplement `<scriptname>` (v�rifiez que le lien `Python` est correctement d�clar� dans l'environnement `PATH`).
- En ex�cutant depuis _Linux Terminal_, tapez `python <scriptname>` ou simplement `./<scriptname>`
(n'oubliez pas de d�finir _executable permissions_ sur `<scriptname>`,
regardez le tutoriel [How to run a Python script in Linux]).
- En ex�cutant depuis [Thonny] - _Python IDE pour d�butants_, chargez `<scriptname>` et ex�cutez-le.
- Souriez :smiley:


[arduino]: <arduino>
[libraries]: <libraries>
[examples]: <examples>
[cgi-bin]: <cgi-bin>
[tools]: <tools>

[jm_PCF8574.py]: <libraries/jm_PCF8574.py>
[jm_LCM2004A_I2C.py]: <libraries/jm_LCM2004A_I2C.py>
[jm_time.py]: <libraries/jm_time.py>

[HelloWorld.ino]: <examples/HelloWorld.ino>

[HelloWorld_explicit.py]: <examples/HelloWorld_explicit.py>
[HelloWorld_compact.py]: <examples/HelloWorld_compact.py>
[Serial_read_char.py]: <examples/Serial_read_char.py>

[jm_LCM2004A_I2C_HelloWorld.py]: <examples/jm_LCM2004A_I2C_HelloWorld.py>
[jm_LCM2004A_I2C_PrintScreen.py]: <examples/jm_LCM2004A_I2C_PrintScreen.py>
[jm_LCM2004A_I2C_charset.py]: <examples/jm_LCM2004A_I2C_charset.py>
[jm_LCM2004A_I2C_demo1.ino]: <https://github.com/jmparatte/jm_LCM2004A_I2C/blob/master/examples/jm_LCM2004A_I2C_demo1/jm_LCM2004A_I2C_demo1.ino>

[Arduino]: <https://www.arduino.cc/>
[Python]: <https://www.python.org/>
[Thonny]: <https://thonny.org/>
[MicroPython]: <https://micropython.org/>

[How to run a Python script in Linux]: <https://www.educative.io/answers/how-to-run-a-python-script-in-linux>

[www.markdownguide.org]: <https://www.markdownguide.org/>
[dillinger.io]: <https://dillinger.io/>

[//]: # (
)
