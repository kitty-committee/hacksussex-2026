from machine import Pin
from machine import I2C

john = I2C(1, sda = Pin(15), scl = Pin(14))