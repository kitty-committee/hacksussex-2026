from machine import I2C, Pin

i2c = I2C(0, scl=Pin(1), sda=Pin(0))

print(i2c.scan())
