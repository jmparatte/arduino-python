# Arduino-Python

Arduino-Python est une implémentation Python/MicroPython des bibliothèques Arduino et de la boîte à outils pour diverses plates-formes telles que Raspberry PI et ESP32.

L'objectif principal de ce développement est d'offrir un moyen rapide de migrer des bibliothèques et des programmes Arduino C++ vers Python/MicroPython.


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

peut être traduit en Arduino-Python explicite [HelloWorld_explicit.py], y compris la traduction de la fonction Arduino C++ `main()`:
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

ou peut être traduit en Arduino-Python compact plus court [HelloWorld_compact.py] en excluant le code inutile:
```python
from Arduino import *

Serial.begin()
Serial.println("Hello World!")
Serial.end()
```


## Platformes supportées

| hardware | OS          | `implementation` | `platform` | Arduino architecture |
|----------|-------------|------------------|------------|----------------------|
| PC       | Windows     | `"cpython"`      | `"win32"`  | `ARDUINO_ARCH_WIN32` |
| PC       | Mac OS      | `"cpython"`      | `"macos"`  | `ARDUINO_ARCH_MACOS` |
| PC       | Linux       | `"cpython"`      | `"linux"`  | `ARDUINO_ARCH_LINUX` |
| RPi      | RPi OS      | `"cpython"`      | `"rpios"`  | `ARDUINO_ARCH_RPIOS` |
| ESP32    | MicroPython | `"micropython"`  | `"esp32"`  | `ARDUINO_ARCH_ESP32` |

- PC/Windows est tout PC opérant un [Python] ou [Thonny] récent.
- PC/Mac OS est tout Mac opérant un [Python] ou [Thonny] récent.
- PC/Linux est tout Linux opérant un [Python] ou [Thonny] récent.
- RPi/RPi OS est tout RPi opérant un [Python] ou [Thonny] récent.
- ESP32/MicroPython est tout ESP32, EPS32-S2 ou ESP32-C3 flashé avec un [MicroPython] récent.

- `implementation` est une constante Arduino-Python chargée avant le démarrage de l'application. Cette constante est un raccourci vers `sys.implementation.name`. Sa valeur est `"cpython"` ou `"micropython"`. `implementation` peut être vérifiée avec un code comme celui-ci:
```Python
if implementation=="micropython":
    # execute next code only if MicroPython implementation...
```
- `platform` est une constante Arduino-Python chargée avant le démarrage de l'application. Sa valeur est dérivée de `sys.platform` et d'autres vérifications. `platform` peut être vérifiée avec un code comme celui-ci:
```Python
if platform=="esp32":
    # execute next code only if ESP32 hardware...
```
- `ARDUINO_ARCH_xxxxx` sont des constantes Arduino-Python chargées avant le démarrage de l'application. Leurs valeurs sont toutes `False` mais une seule est `True`. Elles peuvent être vérifiés avec un code comme celui-ci:
```Python
if ARDUINO_ARCH_ESP32:
    # execute next code only if ESP32 hardware...
```


## En-têtes, classes et objets Arduino traduits

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

`Serial` est l'entrée/sortie de la console Arduino. Cet objet est implémenté sur un uart sériel, un usb sériel ou un sériel virtuel. Aucune restriction ne s'applique à l'écriture.

`Serial.write()` accepte 1 argument avec 3 significations différentes:
- `c`, un entier positif de 8 bits écrit sur un seul octet.
Il peut s'agir de la valeur ordinale d'un caractère ou d'un octet de données.
Exemple : `Serial.write(ord('A')) # écriture de l'octet 65`
- `bstr`, un objet Python `bytes` écrit en une série d'octets.
Exemple : `Serial.write(b'hello\r\n') # écrit 7 octets`
- `str`, une chaîne Python unicode convertie en octets utf-8 puis écrite.
Exemple : `Serial.write('é') # écrit 2 octets : b'\xc3\xa9'`

`Serial.print()` accepte 1 argument avec 3 significations différentes :
- `n`, un nombre Python imprimé sous forme de chaîne lisible par l'homme.
Exemple : `Serial.print(65) # écrit la série d'octets b'65'`
- `bstr`, même comportement que `Serial.write()`
- `str`, même comportement que `Serial.write()`

`Serial.write()` et `Serial.print()` renvoient le nombre d'octets écrits.

`Serial.println()` procède de la même manière que `Serial.print()` mais ajoute `b'\r\n'` en fin de ligne.

`Serial0` (Raspberry Pi), `Serial1` et suivants ont les mêmes méthodes que `Serial`.

## Serial.read()

`Serial` est l'entrée/sortie de la console Arduino.
Cet objet est implémenté sur un uart sériel, un usb sériel ou un sériel virtuel.
Des restrictions s'appliquent à la lecture.

`Serial.read()` n'a pas d'argument, il renvoie soit:
- la valeur entière `-1` si aucune donnée n'est disponible.
- un entier positif 8 bits représentant la valeur ordinale d'un caractère ou d'un octet de données.
La valeur ordinale du caractère peut être convertie en `str` par la fonction `chr()`.
Exemple 1 : `str += chr(65) # ajoute 'A' à str`.
Exemple 2 : `bstr += chr(65).encode() # ajoute b'A' à bstr`

Les restrictions sont de 2 types :
- les programmes exécutés via l'IDE [Thonny] ne peuvent pas avoir une véritable lecture de la console caractère par caractère.
Lors de l'exécution du 1er `Serial.read()`, une ligne d'entrée complète est lue, mise en mémoire tampon et complétée par `<CR><LF>`, puis lue caractère par caractère.
Lors de la lecture de la ligne d'entrée, le programme est bloqué et le contrôle n'est pas rendu tant qu'un caractère de fin de ligne n'est pas tapé !
- en pratique, les caractères lus par la console sont limités au jeu de caractères `ascii` 7 bits à l'exclusion des caractères de contrôle et du caractère `<DEL>`.
Un encodeur/décodeur 8 bits vers/depuis le jeu de caractères `ascii` avec somme de contrôle doit être implémenté pour échanger des données sécurisées sans restriction via la console.

`Serial0` (Raspberry Pi), `Serial1` et suivants ont les mêmes méthodes que `Serial` toutefois sans aucune restriction de lecture.

## Folders contents

- [arduino] - Core Arduino traduits en Python
- [libraries] - Librairies Arduino traduites en Python
- [examples] - Exemples Arduino-Python
- [cgi-bin] - Scripts CGI Python pour serveurs Web HTTP
- [tools] - Outils Python

Des informations complémentaires sont données dans chaque dossier.


## Installation

- Créez un dossier de développement `<arduino-python>`.
- Copiez tous les fichiers [arduino] dans le dossier de développement `<arduino-python>`.
- Copiez les autres fichiers à étudier de [libraries] et [examples] dans le dossier de développement `<arduino-python>`.


## Usage basique

- Ouvrez le dossier de développement `<arduino-python>`.
- En exécutant depuis _Windows Command_, tapez `python <scriptname>` ou simplement `<scriptname>` (vérifiez que le lien `Python` est correctement déclaré dans l'environnement `PATH`).
- En exécutant depuis _Linux Terminal_, tapez `python <scriptname>` ou simplement `./<scriptname>`
(n'oubliez pas de définir _executable permissions_ sur `<scriptname>`,
regardez le tutoriel [How to run a Python script in Linux]).
- En exécutant depuis [Thonny] - _Python IDE pour débutants_, chargez `<scriptname>` et exécutez-le.
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
