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
