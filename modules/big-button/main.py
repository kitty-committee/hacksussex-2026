# Imports
import random
from utime import sleep
from utime import time
from machine import Pin
from neopixel import NeoPixel
from puzzlebox import PuzzleBoxModule

module = PuzzleBoxModule(10)
pin = Pin(9, Pin.OUT)
pin.on()

NeedToHold = False
ButtonPressed = False
NumToReleaseOn = 0
TotalTime = 117
Minutes = 0
Seconds = 0

GameStart = 0

StartColour = (0,0,0)
HeldColour = (0,0,0)

# Colours
LionbananaBlue = (20, 20, 100)
LionbananaPink = (20, 100, 20)
LionbananaYellow = (80, 120, 0)
LionbananaGreen = (100, 0, 0)
LionbananaOff = (0, 0, 0)
        
def Setup():
    global StartColour, TotalTime, NeedToHold, GRBled, BigButton, NumToReleaseOn, HeldColour, ButtonPressed, GameStart
    GameStart = time()
    LED = Pin(28, Pin.OUT)
    LED.on()
    NeedToHold = False
    ButtonPressed = False
    NumToReleaseOn = 0
    StartColour = (0,0,0)
    HeldColour = (0,0,0)
    TotalTime = module.time_limit

    # Define the LED pin number (2) and number of LEDs (1)
    GRBled = NeoPixel(Pin(2), 1)

    # Define button parameters
    BigButton = Pin(4, Pin.IN, Pin.PULL_UP)

    

    # Get random number from all colours
    tempNum = random.randint(1, 5)

    # Select start colour
    if tempNum == 1:
        # Yellow - Hold
        StartColour = LionbananaYellow
        NeedToHold = True
    elif tempNum == 2:
        # Blue - Tap
        StartColour = LionbananaBlue
        NeedToHold = False
    elif tempNum == 3:
        # Green - Hold
        StartColour = LionbananaGreen
        NeedToHold = True
    elif tempNum == 4:
        # Pink - Tap
        StartColour = LionbananaPink
        NeedToHold = False
    elif tempNum == 5:
        # Off - Hold
        StartColour = LionbananaOff
        NeedToHold = True

    # Get random number from all colours
    tempNum = random.randint(1, 5)

    if tempNum == 1:
        # Yellow - Release on 3
        HeldColour = LionbananaYellow
        NumToReleaseOn = 3
    elif tempNum == 2:
        # Blue - Release on 2
        HeldColour = LionbananaBlue
        NumToReleaseOn = 2
    elif tempNum == 3:
        # Green - Release on 5
        HeldColour = LionbananaGreen
        NumToReleaseOn = 5
    elif tempNum == 4:
        # Pink - Release on 8
        HeldColour = LionbananaPink
        NumToReleaseOn = 8
    elif tempNum == 5:
        # Off - Release Anytime
        HeldColour = LionbananaOff
        NumToReleaseOn = 0

    return

def GetMinutes(Time):
    global Minutes
    Minutes = Time // 60
    return

def GetSeconds(Time):
    global Seconds
    Seconds = Time % 60
    return

def SetTime(Time):
    GetSeconds(Time)
    GetMinutes(Time)
    return

def Victory():
    module.complete()
    return

def Strike():
    module.strike()
    
    # Set the colour of the LED 
    GRBled.fill(LionbananaOff)

    # Display the colour
    GRBled.write()
    return


def main():
    global ButtonPressed
    # Sets up the module
    Setup()

    # Set the colour of the LED 
    GRBled.fill(StartColour)

    # Display the colour
    GRBled.write()

    gotStruck = False
    while True:

        if ButtonPressed:
            # On release
            if (time() - start) > 0.1:
                ButtonPressed = False
                SetTime(TotalTime - abs(releaseTime))
                if not NeedToHold:
                    Strike()
                elif NumToReleaseOn == 0 and not gotStruck and NeedToHold:
                    Victory()
                    break
                elif Seconds % 10 == NumToReleaseOn and not gotStruck and NeedToHold or Seconds // 10 == NumToReleaseOn and not gotStruck and NeedToHold or Minutes == NumToReleaseOn and not gotStruck and NeedToHold:
                    Victory()
                    break
                elif gotStruck:
                    gotStruck = False
                else:
                    Strike()
                # Set the colour of the LED 
                GRBled.fill(StartColour)

                # Display the colour
                GRBled.write()

        if BigButton.value() == 0:
            if ButtonPressed:
                # Set the colour of the LED 
                GRBled.fill(HeldColour)

                # Display the colour
                GRBled.write()
            releaseTime = GameStart - time()
            sleep(0.2)
            if BigButton.value() != 0 and not NeedToHold and not ButtonPressed:
                Victory()
                break
            elif BigButton.value() != 0 and NeedToHold and not ButtonPressed:
                Strike()
                gotStruck = True
            start = time()
            ButtonPressed = True
    return
        

module.run(main)