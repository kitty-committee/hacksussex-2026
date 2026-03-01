from machine import Pin, PWM
from utime import sleep
from random import randint
from puzzlebox import PuzzleBoxModule


module = PuzzleBoxModule(9)

bluebutton = Pin(19, Pin.IN, Pin.PULL_UP)
redbutton = Pin(21, Pin.IN, Pin.PULL_UP)
yellowbutton = Pin(18, Pin.IN, Pin.PULL_UP)
greenbutton = Pin(20, Pin.IN, Pin.PULL_UP)

bluelight = Pin(12, Pin.OUT, Pin.PULL_DOWN)
redlight =Pin(10, Pin.IN, Pin.PULL_DOWN)
yellowlight = Pin(13, Pin.IN, Pin.PULL_DOWN)
greenlight = Pin(11, Pin.OUT, Pin.PULL_DOWN)

colours = ["b", "r", "y", "g"]

listofflash = []
listofinput = []
listoftrue = []


def blueflash():
    bluelight.on()
    sleep(0.5)
    bluelight.off()

def redflash():
    redlight.on()
    sleep(0.5)
    redlight.off()

def yellowflash():
    yellowlight.on()
    sleep(0.5)
    yellowlight.off()


def greenflash():
    greenlight.on()
    sleep(0.5)
    greenlight.off()

def flash():
    redlight.off()
    bluelight.off()
    greenlight.off()
    yellowlight.off()
    
    while len(listofflash) < 5:
        number = randint(0,150500)
        number = number % 4
        listofflash.append(colours[number])
        for x in listofflash:
            if x == "b":
                blueflash()
                
            if x == "y":
                yellowflash()
                
            if x == "r":
                redflash()

            if x == "g":
                greenflash()
        listoftrue = []
        if(module.strikes == 0):
            for item in listofflash:
                if item == "b":
                    listoftrue.append("r")
                if item == "r":
                    listoftrue.append("b")
                if item == "y":
                    listoftrue.append("g")
                if item == "g":
                    listoftrue.append("y")

        if(module.strikes == 1):
            for item in listofflash:
                if item == "b":
                    listoftrue.append("g")
                if item == "r":
                    listoftrue.append("y")
                if item == "y":
                    listoftrue.append("r")
                if item == "g":
                    listoftrue.append("b")

        if(module.strikes == 2):
            for item in listofflash:
                if item == "b":
                    listoftrue.append("r")
                if item == "r":
                    listoftrue.append("g")
                if item == "y":
                    listoftrue.append("b")
                if item == "g":
                    listoftrue.append("y")

        print(listoftrue)
        listofinput = []
        while(len(listofinput) < len(listofflash)):
            for x in listofflash:
                if bluebutton.value() == 0:
                    listofinput.append("b")
                    blueflash()
                if redbutton.value() == 0:
                    listofinput.append("r")
                    redflash()
                if yellowbutton.value() == 0:
                    listofinput.append("y")
                    yellowflash()
                if greenbutton.value() == 0:
                    listofinput.append("g")
                    greenflash()
        
        print("actual inputs: ")
        print(listofflash)
        print("scrambled inputs:")
        print(listoftrue)
        print("user inputs: ")
        print(listofinput)
        #swap the input list here

        i=0
        while i < len(listofflash):
            if listoftrue[i] != listofinput[i]:
                module.strike()
                
            i += 1
    module.complete()

module.run(flash)
