# Imports
from machine import Pin
from utime import sleep

DELAY = 0.0025

Ones = 0
Tens = 0
Hundreds = 0
Thousands = 0
Minutes = 0
Seconds = 0

First = Pin(18, Pin.OUT)
Second = Pin(19, Pin.OUT)
Third = Pin(20, Pin.OUT)
Fourth = Pin(21, Pin.OUT)

SegA = Pin(2, Pin.OUT)
SegB = Pin(3, Pin.OUT)
SegC = Pin(4, Pin.OUT)
SegD = Pin(5, Pin.OUT)
SegE = Pin(6, Pin.OUT)
SegF = Pin(7, Pin.OUT)
SegG = Pin(8, Pin.OUT)
DecP = Pin(9, Pin.OUT)


def GetMinutes(Time):
    global Minutes
    Minutes = Time // 60
    return


def GetSeconds(Time):
    global Seconds
    Seconds = Time % 60
    return


def GetOnes():
    global Ones
    Ones = Seconds % 10
    return


def GetTens():
    global Tens
    Tens = Seconds // 10
    return


def GetHundreds():
    global Hundreds
    Hundreds = Minutes % 10
    return


def GetThousands():
    global Thousands
    Thousands = Minutes // 10
    return


def DisplayNum(NumToDisplay: int, Digit: int, DP: bool):
    if Digit == 1:
        TempPin = First
    elif Digit == 2:
        TempPin = Second
    elif Digit == 3:
        TempPin = Third
    else:
        TempPin = Fourth

    TempPin.off()
    if DP:
        DecP.on()
    else:
        DecP.off()

    if NumToDisplay == 0:
        SegA.on()
        SegB.on()
        SegC.on()
        SegD.on()
        SegE.on()
        SegF.on()
        SegG.off()
    elif NumToDisplay == 1:
        SegA.off()
        SegB.on()
        SegC.on()
        SegD.off()
        SegE.off()
        SegF.off()
        SegG.off()
    elif NumToDisplay == 2:
        SegA.on()
        SegB.on()
        SegC.off()
        SegD.on()
        SegE.on()
        SegF.off()
        SegG.on()
    elif NumToDisplay == 3:
        SegA.on()
        SegB.on()
        SegC.on()
        SegD.on()
        SegE.off()
        SegF.off()
        SegG.on()
    elif NumToDisplay == 4:
        SegA.off()
        SegB.on()
        SegC.on()
        SegD.off()
        SegE.off()
        SegF.on()
        SegG.on()
    elif NumToDisplay == 5:
        SegA.on()
        SegB.off()
        SegC.on()
        SegD.on()
        SegE.off()
        SegF.on()
        SegG.on()
    elif NumToDisplay == 6:
        SegA.on()
        SegB.off()
        SegC.on()
        SegD.on()
        SegE.on()
        SegF.on()
        SegG.on()
    elif NumToDisplay == 7:
        SegA.on()
        SegB.on()
        SegC.on()
        SegD.off()
        SegE.off()
        SegF.off()
        SegG.off()
    elif NumToDisplay == 8:
        SegA.on()
        SegB.on()
        SegC.on()
        SegD.on()
        SegE.on()
        SegF.on()
        SegG.on()
    else:
        SegA.on()
        SegB.on()
        SegC.on()
        SegD.on()
        SegE.off()
        SegF.on()
        SegG.on()
    return


def TimeToDisplay(Time):
    GetMinutes(Time)
    GetSeconds(Time)

    # Display the ones column
    GetOnes()
    DisplayNum(Ones, 4, False)
    sleep(DELAY)
    Fourth.on()

    # Display the tens column
    GetTens()
    DisplayNum(Tens, 3, False)
    sleep(DELAY)
    Third.on()

    # Display the hundreds column
    GetHundreds()
    DisplayNum(Hundreds, 2, True)
    sleep(DELAY)
    Second.on()

    # Display the thousands column
    GetThousands()
    DisplayNum(Thousands, 1, False)
    sleep(DELAY)
    First.on()


def DisplayNumbers(num):

    # Display the ones column
    DisplayNum(num % 10, 4, False)
    sleep(DELAY)
    Fourth.on()

    # Display the tens column
    DisplayNum((num % 100) // 10, 3, False)
    sleep(DELAY)
    Third.on()

    # Display the hundreds column
    DisplayNum((num // 100) % 10, 2, False)
    sleep(DELAY)
    Second.on()

    # Display the thousands column
    GetThousands()
    DisplayNum(num // 1000, 1, False)
    sleep(DELAY)
    First.on()


def reset_display():
    First.on()
    Second.on()
    Third.on()
    Fourth.on()
