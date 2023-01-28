#!/usr/bin/python3

# https://www.arduino.cc/reference/en/libraries/sd/
# https://docs.arduino.cc/learn/programming/sd-guide#list-files

from Arduino import *
from SD import *

def printDirectory(dir, numTabs=0):

    while True:

        entry = dir.openNextFile()

        if not entry:
            if numTabs==0:
                Serial.println("** Done **")
            return

        for _ in range(0, numTabs):
            Serial.print('\t')

        Serial.print(entry.name())

        if entry.isDirectory():
            Serial.println("/")
            printDirectory(entry, numTabs+1)
        else:
            Serial.print("\t\t")
            Serial.println(entry.size()) #, DEC)

        entry.close()

if __name__=="__main__":

    Serial.begin()

    SD.begin()

    root = SD.open("www")
    printDirectory(root)
    root.rewindDirectory()
    root.close()

    SD.end()

    Serial.end()
