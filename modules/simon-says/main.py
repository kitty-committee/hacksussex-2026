from machine import Pin, PWM
from utime import sleep


bluebutton = Pin(19, Pin.IN, Pin.PULL_UP)
redbutton = Pin(21, Pin.IN, Pin.PULL_UP)
yellowbutton = Pin(18, Pin.IN, Pin.PULL_UP)
greenbutton = Pin(20, Pin.IN, Pin.PULL_UP)

bluelight = Pin(12, Pin.OUT, Pin.PULL_UP)
redlight =Pin(10, Pin.IN, Pin.PULL_UP)
yellowlight = Pin(13, Pin.IN, Pin.PULL_UP)
greenlight = Pin(11, Pin.OUT, Pin.PULL_DOWN)

while True:
    print("hi")
    if(bluebutton.value() == 0):
        print("blue on")