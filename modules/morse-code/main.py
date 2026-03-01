from machine import Pin, PWM
import random
from utime import sleep
from puzzlebox import PuzzleBoxModule

module = PuzzleBoxModule(6, id=1,sda=6,scl=7,complete_pin=10)

pin = Pin("LED", Pin.OUT)

# Create a Pin object named "buzzer" connected to GPIO pin 16 as an output



buttonlight = Pin(2, Pin.OUT)
buzzer = Pin(9, Pin.OUT)
toggled = False
timer = 0.25
longtimer = 1
light = Pin(5, Pin.OUT)
button = Pin(20, Pin.IN, Pin.PULL_DOWN)
input1 = Pin(18, Pin.IN, Pin.PULL_UP)
input2 = Pin(19, Pin.IN, Pin.PULL_UP)
input3 = Pin(21, Pin.IN, Pin.PULL_UP)
input4 = Pin(22, Pin.IN, Pin.PULL_UP)

dictionary_no_cheating = {
    'yes':1,
    'eye':2,
    'aye':3,
    'abs':4,
    'ebb':1,
    'eve':2,
    'bee':3,
    'all':4,
    'saw':1,
    'sat':2,
    'sit':3,
    'see':4,

}

wordlist = ["yes", "eye", "aye", "abs", "ebb", "eve", "bee", "all", "saw", "sat", "sit", "see"]

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

def swapintomorse(x):

    buttonlight.off()

    morselist = []
    conversionlist = []
    list = x
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

def askquestion():

    buttonlight.off()
    turnoff()
    num = random.randint(0,11)
    word = wordlist[num]
    print(word)
    swapintomorse(word)
    correctbutton = dictionary_no_cheating.get(word, None)
    print(correctbutton)
    while(input1.value() != 0 or input2.value() != 0 or input3.value() != 0 or input4.value() != 0):
        if(correctbutton == 1 and input1.value() == 0):
            #send correct
            module.complete()
            
        if(correctbutton == 2 and input2.value() == 0):
                #send correct
                module.complete()
                
        if(correctbutton == 3 and input3.value() == 0):
                #send correct
                module.complete()
                
        if(correctbutton == 4 and input4.value() == 0):
                #send correct
                module.complete()
            

        if(correctbutton != 1 and input1.value() == 0):
            #send incorrect
            module.strike()
        if(correctbutton != 2 and input2.value() == 0):
                #send incorrect
                module.strike()
        if(correctbutton != 3 and input3.value() == 0):
                #send incorrect
                module.strike()
        if(correctbutton != 4 and input4.value() == 0):
                #send incorrect
                module.strike()
                
        if(button.value() == 1):
            swapintomorse(word)


module.run(askquestion)