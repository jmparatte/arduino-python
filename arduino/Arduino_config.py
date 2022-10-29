
# Arduino config
# ==============

from Arduino_defines import *

if ARDUINO_ARCH_WIN32:

# WIN32 possible options:
# ----------------------
#SERIAL1_COM_PORT = 'COM4'
#SERIAL1_COM_PORT = (__argc==2 ? __argv[1] : "")
#SERIAL1_COM_PORT = (__argc>=2 ? __argv[2-1] : "")
#SD_ROOTNAME = 'A:'
#SD_ROOTNAME = 'H:\\SD'
#SD_ROOTNAME = "%CD%"
#SD_ROOTNAME = BUILD_SOURCE_PATH
#SD_ROOTNAME = (__argc==2 ? __argv[1] : "")

    LED_BUILTIN = -1 # no built-in LED installed
    SERIAL1_COM_PORT = 'COM91' # FTDI/Win32
    SD_ROOTNAME = '.' # start folder of app
    #WIRE_I2C_NUM = n # I2C device not available
    #WIRE_SCL_PIN = n
    #WIRE_SDA_PIN = n

elif ARDUINO_ARCH_MACOS:

    LED_BUILTIN = -1 # no built-in LED installed
    SERIAL1_COM_PORT = '/dev/ttyUSB0' # FTDI/Linux
    SD_ROOTNAME = '.' # start folder of app
    #WIRE_I2C_NUM = n # I2C device not available
    #WIRE_SCL_PIN = n
    #WIRE_SDA_PIN = n

elif ARDUINO_ARCH_LINUX:

    LED_BUILTIN = -1 # no built-in LED installed
    SERIAL1_COM_PORT = '/dev/ttyUSB0' # FTDI/Linux
    SD_ROOTNAME = '.' # start folder of app
    WIRE_I2C_NUM = 1 # device i2c-1
    #WIRE_SCL_PIN = n
    #WIRE_SDA_PIN = n

elif ARDUINO_ARCH_RPIOS:

    # RaspberryPi 3B+/4:
    # -----------------
    LED_BUILTIN = -1 # no built-in LED installed
    SERIAL0_UART_NUM = 0 # device UART0
    SERIAL0_TX_PIN = 8 # GPIO 14
    SERIAL0_RX_PIN = 10 # GPIO 15
    SERIAL1_COM_PORT = '/dev/ttyUSB0' # FTDI/Linux
    SD_ROOTNAME = '.' # start folder of app
    WIRE_I2C_NUM = 1 # device i2c-1
    #WIRE_SCL_PIN = 5 # GPIO 3, do not change !
    #WIRE_SDA_PIN = 3 # GPIO 2, do not change !

elif ARDUINO_ARCH_ESP32:

    # LOLIN D1 mini - ESP-8266EX:
    # --------------------------
    #   pin gpio name     name gpio pin row
    #   o------>               <------o extern
    #          +---------------+
    #   1>  RST|RST       U0TXD|TX  <16
    #   2>   A0|A0        U0RXD|RX  <15
    #   3>   16|D0       D1/SCL|5   <14
    #   4>   14|D5/SCK   D2/SDA|4   <13
    #   5>   12|D6/MISO      D3|0   <12
    #   6>   13|D7/MOSI  D4/LED|2   <11
    #   7>   15|D8          GND|GND <10
    #   8>  3V3|3V3        VBUS|VBUS <9
    #          +---------------+
    #   LED=D4=GPIO2=PIN11
    #   SCL=D1=GPIO5=PIN14, SDA=D2=GPIO4=PIN13
    #   SCK=D5=GPIO14=PIN4, MISO=D6=GPIO12=PIN5, MOSI=D7=GPIO13=PIN6
    #   D0=GPIO16=PIN3, D3=GPIO0=PIN12, D8=GPIO15=PIN7
    #   A0=PIN2

    # LOLIN S2 mini - ESP32-S2:
    # ------------------------
    #   pin gpio gpio     gpio gpio pin row
    #   ox----->               <-----xo extern
    #   xo--------->       <---------ox intern
    #          +---+-------+---+
    #   1>   EN|  1|       |40 |39  <16
    #   2>    3|  2|       |38 |37  <15
    #   3>    5|  4|       |36 |35  <14
    #   4>    7|  6|       |34 |33  <13
    #   5>    9|  8|       |21 |18  <12
    #   6>   11| 10|       |17 |16  <11
    #   7>   12| 13|       |GND|GND <10
    #   8>  3V3| 14|       |15 |VBUS <9
    #          +---+-------+---+
    #   LED=GPIO15, BTN=GPIO0

    LED_BUILTIN = 15 # GPIO 15 (D1 mini GPIO 2)
    #SERIAL1_UART_NUM = 1 # device UART1
    #SERIAL1_TX_PIN = 10
    #SERIAL1_RX_PIN = 9
    SERIAL1_UART_NUM = 1 # device UART1
    SERIAL1_TX_PIN = 3
    SERIAL1_RX_PIN = 5
    SD_ROOTNAME = '' # Flash memory folder
    WIRE_I2C_NUM = -1 # SoftI2C
    WIRE_SCL_PIN = 35 # GPIO 35 (D1 mini GPIO 5)
    WIRE_SDA_PIN = 33 # GPIO 33 (D1 mini GPIO 4)

else:
    pass
