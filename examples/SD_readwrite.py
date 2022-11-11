#!/usr/bin/python3

# https:#www.arduino.cc/reference/en/libraries/sd/
# https:#docs.arduino.cc/learn/programming/sd-guide#read-and-write

from Arduino import *
from SD import *

Serial.begin()

SD.begin()

# open the file. note that only one file can be open at a time,
# so you have to close this one before opening another.

myFile = SD.open("test.txt", FILE_WRITE)
#raise Exception("stop")

# if the file opened okay, write to it:

if myFile:

    Serial.print("Writing to test.txt...")
    myFile.println("testing 1, 2, 3.")
    # close the file:
    myFile.close()
    Serial.println("done.")

else:

    # if the file didn't open, print an error:
    Serial.println("error opening test.txt")

# re-open the file for reading:

myFile = SD.open("test.txt")
#raise Exception("stop")

if myFile:

    Serial.println("test.txt:")
    # read from the file until there's nothing else in it:
    while myFile.available():
        Serial.write(myFile.read())
    # close the file:
    myFile.close()

else:

    # if the file didn't open, print an error:
    Serial.println("error opening test.txt")

SD.end()

Serial.end()
