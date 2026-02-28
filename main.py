from machine import Pin, PWM
from utime import sleep
pin = Pin("LED", Pin.OUT)

# Create a Pin object named "buzzer" connected to GPIO pin 16 as an output

light = Pin(9, Pin.OUT)
buzzer = Pin(12, Pin.OUT)
toggled = False

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



while True:

  # Turn the buzzer on
  toggle()
  # Pause the program execution for 1 second
  sleep(1)
  # Turn the buzzer off
  toggle()
  # Pause the program execution for 1 second
  sleep(1)