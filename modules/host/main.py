from machine import I2C, Pin
from utime import sleep

try:
    from typing import Literal
except ImportError:
    pass

TIME_LIMIT = 300  # 5 minutes

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)

switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
strike_1 = Pin(2, Pin.OUT)
strike_2 = Pin(3, Pin.OUT)
buzzer = Pin(1, Pin.OUT)

state: "Literal['pregame'] | Literal['playing'] | Literal['postgame']" = "pregame"
modules: list[int] = []
completed = 0
strikes = 0


def send_event(id: int, payload: bytes):
    buf = bytearray(1 + len(payload))
    buf[0] = id
    buf[1:] = payload

    for module in modules:
        i2c.writeto_mem(module, 0, buf)


def start_pregame():
    global state, completed, strikes
    send_event(0x02, b"")  # Reset event
    state = "pregame"
    completed = 0
    strikes = 0

    strike_1.off()
    strike_2.off()
    buzzer.off()


def pregame():
    global modules

    sleep(1)

    # Scan for modules every second
    modules = i2c.scan()

    if switch.value() == 1:
        start_game()


def start_game():
    global state
    state = "playing"
    buzzer.on()
    sleep(0.5)
    buzzer.off()
    send_event(0x01, int.to_bytes(TIME_LIMIT, 2, "little"))  # Start event


def playing():
    global state, completed, strikes

    sleep(0.1)

    for module in modules:
        status = i2c.readfrom_mem(module, 7, 1)[0]
        # Module completed
        if status == 0x01:
            completed += 1
        # Module strike
        elif status == 0x02:
            strikes += 1
            # Update strike indicators
            strike_1.value(strikes >= 1)
            strike_2.value(strikes >= 2)

    # Check if should change state

    if switch.value() == 0:
        start_pregame()

    if completed >= len(modules):
        state = "postgame"
        for _ in range(3):
            buzzer.on()
            sleep(0.1)
            buzzer.off()
            sleep(0.1)

    if strikes >= 3:
        state = "postgame"
        for _ in range(3):
            buzzer.on()


def postgame():
    global state

    sleep(1)

    if switch.value() == 0:
        start_pregame()


start_pregame()
while True:
    if state == "pregame":
        pregame()
    elif state == "playing":
        playing()
    elif state == "postgame":
        postgame()
