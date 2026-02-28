from machine import Pin, PWM
from utime import sleep
pin = Pin("LED", Pin.OUT)

# Create a Pin object named "buzzer" connected to GPIO pin 16 as an output

buttonlight = Pin(9, Pin.OUT)
buzzer = Pin(12, Pin.OUT)
toggled = False
timer = 0.75
longtimer = 1.5
light = Pin(5, Pin.OUT)
button = Pin(20, Pin.IN, Pin.PULL_DOWN)


translation = {'a': '.-', 
               'b': '-...', 
               'c': '-.-.', 
               'd': '-..', 
               'e': '.', 
               'f': '..-.', 
               'g': '--.', 
               'h': '....',
               'i': '..', 
               'j': '.---', 
               'k': '-.-', 
               'l': '.-..', 
               'm': '--', 
               'n': '-.', 
               'o': '---', 
               'p': '.--.',
               'q': '--.-', 
               'r': '.-.', 
               's': '...', 
               't': '-', 
               'u': '..-', 
               'v': '...-', 
               'w': '.--', 
               'x': '-..-',
               'y': '-.--', 
               'z': '--..', 
               '1': '.----', 
               '2': '..---', 
               '3': '...--', 
               '4': '....-', 
               '5': '.....',
               '6': '-....', 
               '7': '--...', 
               '8': '---..', 
               '9': '----.', 
               '0': '-----'}

def toggle():
    global toggled
    if(toggled):
        turnoff()
    else:
        turnon()

def turnoff():
    light.off()
    buzzer.low()
    global toggled
    toggled = False

def turnon():
    light.on()
    buzzer.high()
    global toggled
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
    sleep(longtimer)

def lettergap():
    sleep((longtimer + timer) / 2)

def swapmorse():

    buttonlight.off()

    temp = "hi"

    morselist = []
    conversionlist = []
    list = temp
    for char in list:
        list.lower()
        morselist.append(translation.get(char, None))
        morselist.append('/')

    for item in morselist:
        for char in item:
            conversionlist.append(char)

    outputmorse(conversionlist)

def outputmorse(x):
    for item in x:
        if(item == "."):
            shortbeep()
        else:
            if(item == "-"):
                longbeep()
            else:
                if item == "/":
                    lettergap()


    buttonlight.on()

buttonlight.on()
turnoff()
while True:
    if button.value() == 1:
        swapmorse()
