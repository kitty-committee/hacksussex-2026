from machine import PWM, Pin
from utime import sleep_ms

nier = [
    (587, 300),  # D5
    (622, 300),  # D#5
    (932, 300),  # A#5
    (587, 300),  # D5
    (622, 300),  # D#5
    (932, 300),  # A#5
    (587, 300),  # D5
    (622, 300),  # D#5
    (932, 300),  # A#5
    (523, 1000),  # C5
    (1174, 300),  # D6
    (1244, 300),  # D#6
    (1244, 1000),  # D#6
    (1244, 300),  # D#6
    (1174, 300),  # D6
    (932, 300),  # A#5
    (783, 300),  # G5
    (1046, 1400),  # C6
    (1174, 300),  # D6
    (1244, 300),  # D#6
    (1244, 1000),  # D#6
    (1244, 300),  # D#6
    (1174, 300),  # D6
    (932, 300),  # A#5
    (783, 300),  # G5
    (1567, 1400),  # G6
]

lose = [
    (587, 500),  # D5
    (554, 500),  # C#5
    (523, 500),  # C5
    (493, 1000),  # B4
]

win = [
    (523, 150),  # C5
    (659, 150),  # E5
    (784, 150),  # G5
    (1047, 600),  # C6
]

activate = [
    (392, 150),  # G4
    (440, 150),  # A4
    (494, 150),  # B4
    (523, 400),  # C5
]

deactivate = [
    (523, 150),  # C5
    (494, 150),  # B4
    (440, 150),  # A4
    (392, 400),  # G4
]

pin = Pin(13, Pin.OUT)  # create a Pin object for the pin you want to use
pwm = PWM(pin)  # create a PWM object on a pin


def play(track: list[tuple[int, int]]):
    for freq, duration in track:
        pwm.duty_u16(10000)
        pwm.freq(freq)
        sleep_ms(duration)
        pwm.duty_u16(0)
        sleep_ms(50)

    pwm.deinit()
