from machine import UART, Pin
from utime import sleep, ticks_diff, ticks_ms, time

import display
import music

try:
    from typing import Literal
except ImportError:
    pass

TIME_LIMIT = 60  # seconds

# ---------- UART protocol constants ----------
BAUD_RATE = 115_200
START_BYTE = 0xAA
BROADCAST = 0xFF  # address used to reach all modules at once

# Host → module commands
CMD_NOOP = 0x00  # no-op (also used as announce from module)
CMD_START = 0x01  # start game  [time_lo, time_hi]
CMD_RESET = 0x02  # reset / end game
CMD_STRIKE = 0x03  # strike update  [strikes_lo, strikes_hi]
CMD_POLL = 0x10  # request status (module replies with its status byte)

# Module → host status codes (reply to CMD_POLL)
STATUS_IDLE = 0x00
STATUS_COMPLETE = 0x01
STATUS_STRIKE = 0x02
STATUS_LOSE = 0x03
# ---------------------------------------------

uart = UART(1, baudrate=BAUD_RATE, tx=Pin(8), rx=Pin(9))

switch = Pin(10, Pin.IN, Pin.PULL_UP)
strike_1 = Pin(13, Pin.OUT)
strike_2 = Pin(22, Pin.OUT)

state: "Literal['pregame'] | Literal['playing'] | Literal['postgame']" = "pregame"
modules: list[int] = []
timer_end = 0
completed = 0
strikes = 0


# ---------- low-level packet helpers ----------


def _checksum(data: bytes) -> int:
    """XOR checksum over the supplied bytes."""
    result = 0
    for b in data:
        result ^= b
    return result


def _send_packet(addr: int, cmd: int, data: bytes = b"") -> None:
    """Transmit one framed packet on the UART bus."""
    core = bytes([addr, cmd, len(data)]) + data
    uart.write(bytes([START_BYTE]) + core + bytes([_checksum(core)]))


def _recv_packet(timeout_ms: int = 20):
    """Read one packet from the UART bus, returning (addr, cmd, data) or None."""
    start = ticks_ms()
    buf = bytearray()
    while ticks_diff(ticks_ms(), start) < timeout_ms:
        if uart.any():
            b = uart.read(1)[0]
            if not buf and b != START_BYTE:
                continue  # wait for frame start
            buf.append(b)
            if len(buf) >= 4:
                addr, cmd, length = buf[1], buf[2], buf[3]
                expected_total = 5 + length  # START + addr + cmd + len + data + csum
                if len(buf) == expected_total:
                    payload = bytes(buf[4 : 4 + length])
                    csum = buf[4 + length]
                    if csum == _checksum(bytes([addr, cmd, length]) + payload):
                        return addr, cmd, payload
                    else:
                        buf.clear()  # bad checksum – discard and resync
    return None


def _poll_module(addr: int) -> int:
    """Ask a single module for its status. Returns the status byte (0x00 on timeout)."""
    _send_packet(addr, CMD_POLL)
    result = _recv_packet(timeout_ms=20)
    if result is not None:
        _, status, _ = result
        return status
    return STATUS_IDLE


# ---------- game-level helpers ----------


def send_event(cmd: int, payload: bytes) -> None:
    """Broadcast a command to every module."""
    _send_packet(BROADCAST, cmd, payload)
    sleep(0.005)  # short gap so all modules can process before next transmission


def start_pregame() -> None:
    global state, completed, strikes
    modules.clear()
    send_event(CMD_RESET, b"")  # tell every module to reset
    state = "pregame"
    completed = 0
    strikes = 0
    print("Pregame entered.")
    strike_1.off()
    strike_2.off()


def pregame() -> None:
    """Listen for module announce packets and wait for the start switch."""
    global modules

    display.DisplayNum(len(modules), 1, False)

    # Collect announce packets for up to 250 ms, then check the switch.
    deadline = ticks_ms() + 250
    while ticks_diff(deadline, ticks_ms()) > 0:
        result = _recv_packet(timeout_ms=10)
        if result is not None:
            addr, cmd, _ = result
            # Modules broadcast CMD_NOOP (announce) during pregame.
            if cmd == CMD_NOOP and addr not in modules:
                modules.append(addr)
                print(f"Module discovered: {addr:#04x}")

    if switch.value() == 0:
        start_game()


def start_game() -> None:
    global state, timer_end
    state = "playing"
    print("Game started!")
    music.play(music.START)
    send_event(CMD_START, int.to_bytes(TIME_LIMIT, 2, "little"))
    timer_end = time() + TIME_LIMIT


def playing() -> None:
    global state, completed, strikes

    remaining = timer_end - time()
    display.TimeToDisplay(remaining)

    for module in modules:
        status = _poll_module(module)
        # Module completed
        if status == STATUS_COMPLETE:
            completed += 1
            music.play(music.COMPLETE)
        # Module strike
        elif status == STATUS_STRIKE:
            strikes += 1
            send_event(CMD_STRIKE, int.to_bytes(strikes, 2, "little"))
            strike_1.value(strikes >= 1)
            strike_2.value(strikes >= 2)
            music.play(music.STRIKE)
        # Module triggered immediate loss
        elif status == STATUS_LOSE:
            strikes = 3

    # Check state transitions.
    if switch.value() == 1:
        music.play(music.STOP)
        start_pregame()
        return

    if completed >= len(modules):
        state = "postgame"
        print("Player wins!")
        music.play(music.WIN)
        sleep(0.1)
        return

    if strikes >= 3 or remaining <= 0:
        state = "postgame"
        print("Player loses!")
        music.play(music.LOSE)


def postgame() -> None:
    sleep(1)
    if switch.value() == 1:
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
