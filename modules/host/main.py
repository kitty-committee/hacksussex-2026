from machine import I2C, Pin
from utime import sleep, time

import display
import music

try:
    from typing import Literal
except ImportError:
    pass

TIME_LIMIT = 30  # 5 minutes

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)

switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
strike_1 = Pin(17, Pin.OUT)
strike_2 = Pin(16, Pin.OUT)

state: "Literal['pregame'] | Literal['playing'] | Literal['postgame']" = "pregame"
modules: list[int] = []
timer_end = 0
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

    print("Pregame entered.")

    strike_1.off()
    strike_2.off()


def pregame():
    global modules

    display.DisplayNum(len(modules), 1, False)
    sleep(0.25)

    # Scan for modules every second
    modules = i2c.scan()

    if switch.value() == 1:
        start_game()


def start_game():
    global state, timer_end
    state = "playing"
    print("Game started!")
    music.play(music.START)
    send_event(0x01, int.to_bytes(TIME_LIMIT, 2, "little"))  # Send start event
    timer_end = time() + TIME_LIMIT


def playing():
    global state, completed, strikes

    remaining = timer_end - time()
    display.TimeToDisplay(remaining)

    for module in modules:
        status = i2c.readfrom_mem(module, 7, 1)[0]
        # Module completed
        if status == 0x01:
            completed += 1
            music.play(music.COMPLETE)
        # Module strike
        elif status == 0x02:
            strikes += 1
            send_event(0x03, int.to_bytes(strikes, 2, "little"))  # Send strike event to all modules
            # Update strike indicators
            strike_1.value(strikes >= 1)
            strike_2.value(strikes >= 2)
            music.play(music.STRIKE)
        elif status == 0x03:
            strikes = 3  # Immediate loss

    # Check if should change state

    if switch.value() == 0:
        music.play(music.STOP)
        start_pregame()

    if completed > len(modules):
        state = "postgame"
        print("Player wins!")
        music.play(music.WIN)
        sleep(0.1)

    if strikes >= 3 or remaining <= 0:
        state = "postgame"
        print("Player loses!")
        music.play(music.LOSE)


def postgame():
    global state

    sleep(1)

    if switch.value() == 0:
        start_pregame()
        music.play(music.STOP)


display.reset_display()
start_pregame()
while True:
    if state == "pregame":
        pregame()
    elif state == "playing":
        playing()
    elif state == "postgame":
        postgame()
