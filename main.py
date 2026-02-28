from machine import Pin, PWM
from utime import sleep
pin = Pin("LED", Pin.OUT)

# Create a Pin object named "buzzer" connected to GPIO pin 16 as an output

light = Pin(9, Pin.OUT)
buzzer = Pin(12, Pin.OUT)
toggled = False
timer = 0.75
longtimer = 1.5

def toggle():
    global toggled
    if(toggled):
        light.off()
        buzzer.low()
        toggled = False
    else:
        light.on()
        buzzer.high()
        toggled = True


def longbeep():
    toggle()
    sleep(longtimer)
    toggle()
    sleep(timer)

def shortbeep():
    toggle()
    sleep(timer)
    toggle()
    sleep(timer)

def wordgap():
    sleep(2)


while True:
    longbeep()
    shortbeep()
    shortbeep()
    wordgap()
    longbeep()