from machine import Pin, PWM
from utime import sleep, time, ticks_ms, ticks_diff

#set up pins
servo = PWM(Pin(22))
servo.freq(50)
button = Pin(12, Pin.IN, Pin.PULL_UP)

#set up variables
cap_level = 0
min_angle = 0
max_angle = 180
angle = min_angle
last_time = time()
increment = 10
angle = 0


#charge control
def move_servo(position, min_pulse = 500, max_pulse = 2500):
    motor_speed = (max_pulse-min_pulse)/180
    pulse = motor_speed * position + min_pulse
    duty = int(pulse/0.305)
    servo.duty_u16(duty)
    


move_servo(0)

while(angle < 180):
    angle = angle+1
    move_servo(angle)
    sleep(0.1)






    




