from machine import Pin, PWM
from utime import sleep, time, ticks_ms, ticks_diff

#set up pins
servo = PWM(Pin(22))
servo.freq(50)
button = Pin(2, Pin.IN, Pin.PULL_UP)
led = Pin(4, Pin.OUT)

#set up variables
min_angle = 0
max_angle = 180
angle = max_angle
increment = 1
down_time = 0.1
completed = False
reset = increment
warning = 30
caution = False

#charge control
def move_servo(position, min_pulse = 500, max_pulse = 2500):
    motor_speed = (max_pulse-min_pulse)/180
    pulse = motor_speed * position + min_pulse
    duty = int(pulse/0.305)
    servo.duty_u16(duty)

#led control



move_servo(angle)
sleep(0.5)

while(angle >= min_angle and not completed):
    led.off()

    if button.value() == 0:
        if angle > max_angle - reset:
            angle = max_angle
            move_servo(angle)
        else:
            angle = angle + reset
            move_servo(angle)
        sleep(down_time/2)

    else:
        angle = angle-increment
        move_servo(angle)
        sleep(down_time)

    if angle < min_angle + warning:
        caution = True
    else:
        caution = False


    if caution:
        sleep(0.025)
        led.on()
        sleep(0.025)
    

    
    










    




