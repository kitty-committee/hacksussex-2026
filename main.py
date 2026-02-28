from machine import I2C,Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import time
import random
# Define LCD I2C pins/BUS/address
SDA = 14
SCL = 15
I2C_BUS = 1
LCD_ADDR = 0x27

led = Pin(9, Pin.OUT)
# Define LCD rows/columns
LCD_NUM_ROWS = 2
LCD_NUM_COLS = 16

# Set up LCD I2C
lcdi2c = I2C(I2C_BUS, sda=Pin(SDA), scl=Pin(SCL), freq=400000)
lcd = I2cLcd(lcdi2c, LCD_ADDR, LCD_NUM_ROWS, LCD_NUM_COLS)



# Set up column pins (inputs)
key1 = Pin(11, Pin.IN, Pin.PULL_DOWN)
key2 = Pin(10, Pin.IN, Pin.PULL_DOWN)
key3 = Pin(13, Pin.IN, Pin.PULL_DOWN)
key4 = Pin(12, Pin.IN, Pin.PULL_DOWN)



def fatextra(input,pattern):
    for i in range(0,4):
        if pattern[i] == "A" and input[i] == "G":
            pass
        elif pattern[i] == "G" and input[i] == "B":
            pass
        elif pattern[i] == "B" and input[i] == "A":
            pass
        else:
            return "fail"
    return "win"

def getInput(attack):
    display = ["?","?","?","?","?","?"]
    selectednums = []
    random1 = 1
    selectednums.append(1)
    display[random1] = attack[random1]
    loop = True
    while loop == True:
        random2 = random.randrange(0,5)
        if random2 not in selectednums:
            selectednums.append(random2)
            display[random2] = attack[random2]
            loop = False
    loop = True
    while loop == True:
        random3 = random.randrange(0,5)
        if random3 not in selectednums:
            selectednums.append(random3)
            display[random3] = attack[random3]
            loop = False
    return display

def generateAttack():
    attackNum = random.randrange(1,5)
    if attackNum == 1:
        attack = ["B","B","A","B","B","A"]
    elif attackNum == 2:
        attack = ["A","B","B","B","B","B"]
    elif attackNum == 3:
        attack = ["G","B","G","G","B","G"]
    elif attackNum == 4:
        attack = ["A","G","G","A","G","G"]
    elif attackNum == 5:
        attack = ["G","B","A","G","B","A"]
    return attack
    
def start():
    num = generateAttack()
    temp = ""
    templist = []
    lcd.clear()
    display = (getInput(num))
    displaystr = display[0] + display[1] +display[2] +display[3] +display[4] +display[5] 
    lcd.putstr(displaystr)
    while (len(temp) < 6):
            if key1.value() == 1:
                temp = temp + 'A'
                templist.append("A")
                lcd.clear()
                lcd.putstr(temp)
                time.sleep(0.5)

            if key2.value() == 1:
                temp = temp + 'G'
                templist.append("G")
                lcd.clear()
                lcd.putstr(temp)
                time.sleep(0.5)
            if key3.value() == 1:
                temp = temp + 'B'
                templist.append("B")
                lcd.clear()
                lcd.putstr(temp)
                time.sleep(0.5)
            if key4.value() == 1:
                temp = temp + 'N/A'
                templist.append("N/A")
                lcd.clear()
                lcd.putstr(temp)
                time.sleep(0.5)
                
                
    ans = fatextra(templist,num)      
    if ans == "win":  
        lcd.clear()
        lcd.putstr(ans)
        led.on()
    else:
        lcd.clear()
        lcd.putstr(ans)
        time.sleep(5)
        start()

    # Run our function

start()