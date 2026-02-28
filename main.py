from machine import Pin, PWM
from utime import sleep
pin = Pin("LED", Pin.OUT)

# Create a Pin object named "buzzer" connected to GPIO pin 16 as an output

buzzer = Pin(12, Pin.OUT)



while True:

  # Turn the buzzer on
  buzzer.high()
  # Pause the program execution for 1 second
  sleep(1)
  # Turn the buzzer off
  buzzer.low()
  # Pause the program execution for 1 second
  sleep(1)