"""PuzzleBox module library – UART transport.

All modules share a single UART bus with the host.  Each module is assigned
a unique 1-byte address (1–254).  The host polls modules individually; 0xFF
is a broadcast address used for events that every module must process.

Packet format (bytes):
  [0xAA] [ADDR] [CMD] [LEN] [DATA × LEN] [XOR_CHECKSUM]
where CHECKSUM = XOR of ADDR, CMD, LEN, and every DATA byte.
"""

try:
    from typing import Any, Callable
except ImportError:
    pass

import _thread

from machine import UART, Pin, reset
from utime import sleep, ticks_diff, ticks_ms

# ---------- protocol constants (must match main.py) ----------
START_BYTE = 0xAA
BROADCAST = 0xFF

CMD_NOOP = 0x00  # also doubles as the announce beacon
CMD_START = 0x01
CMD_RESET = 0x02
CMD_STRIKE = 0x03
CMD_POLL = 0x10

STATUS_IDLE = 0x00
STATUS_COMPLETE = 0x01
STATUS_STRIKE = 0x02
STATUS_LOSE = 0x03
# ------------------------------------------------------------


class PuzzleBoxModule:
    """A module that communicates with the PuzzleBox host over UART."""

    # UART peripheral used to communicate with the host.
    uart: UART

    # This module's bus address (1–254).
    addr: int

    # Set to True once the host sends CMD_START.
    started: bool = False

    # Time limit received from the host (seconds).
    time_limit: int = 0

    # Optional output pin that lights up when the module is solved.
    complete_pin: "None | Pin"

    # Strike count as reported by the host.
    strikes: int = 0

    # Pending status to report on the next poll.  Written by puzzle logic;
    # read and cleared by the UART background thread.
    _status: int = STATUS_IDLE

    # Lock that protects _status from concurrent access.
    _lock: "Any"

    def __init__(
        self,
        addr: int,
        *,
        id: int = 1,
        tx: int = 8,
        rx: int = 9,
        baud: int = 115_200,
        complete_pin: "int | None" = None,
    ) -> None:
        self.addr = addr
        self.complete_pin = Pin(complete_pin, Pin.OUT) if complete_pin is not None else None
        self._lock = _thread.allocate_lock()
        self.uart = UART(id, baudrate=baud, tx=Pin(tx), rx=Pin(rx))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _checksum(self, data: bytes) -> int:
        result = 0
        for b in data:
            result ^= b
        return result

    def _send_packet(self, cmd: int, data: bytes = b"") -> None:
        """Transmit a packet addressed from this module to the host."""
        core = bytes([self.addr, cmd, len(data)]) + data
        self.uart.write(bytes([START_BYTE]) + core + bytes([self._checksum(core)]))

    def _recv_packet(self, timeout_ms: int = 10):
        """Read one incoming packet, returning (addr, cmd, data) or None."""
        start = ticks_ms()
        buf = bytearray()
        while ticks_diff(ticks_ms(), start) < timeout_ms:
            if self.uart.any():
                b = self.uart.read(1)[0]
                if not buf and b != START_BYTE:
                    continue
                buf.append(b)
                if len(buf) >= 4:
                    addr, cmd, length = buf[1], buf[2], buf[3]
                    expected_total = 5 + length
                    if len(buf) == expected_total:
                        payload = bytes(buf[4 : 4 + length])
                        csum = buf[4 + length]
                        if csum == self._checksum(bytes([addr, cmd, length]) + payload):
                            return addr, cmd, payload
                        else:
                            buf.clear()  # bad checksum – resync
        return None

    def _handle_command(self, cmd: int, data: bytes) -> None:
        """Process one inbound command from the host."""
        if cmd == CMD_START:
            print("Received CMD_START")
            self.time_limit = int.from_bytes(data[:2], "little")
            self.started = True
            self.strikes = 0
            with self._lock:
                self._status = STATUS_IDLE

        elif cmd == CMD_RESET:
            print("Received CMD_RESET – resetting...")
            reset()

        elif cmd == CMD_STRIKE:
            print("Received CMD_STRIKE")
            self.strikes = int.from_bytes(data[:2], "little")

        elif cmd == CMD_POLL:
            with self._lock:
                status = self._status
                self._status = STATUS_IDLE  # clear after reporting
            self._send_packet(status)

        elif cmd == CMD_NOOP:
            pass  # nothing to do

        else:
            print(f"Unknown command: {cmd:#04x}")

    def _uart_thread(self) -> None:
        """Background thread: receive packets and respond to polls."""
        while True:
            result = self._recv_packet(timeout_ms=10)
            if result is not None:
                addr, cmd, data = result
                if addr == self.addr or addr == BROADCAST:
                    self._handle_command(cmd, data)

    def _announce(self) -> None:
        """Broadcast an announce beacon so the host can discover this module."""
        self._send_packet(CMD_NOOP)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, fn: "Callable[[], Any]") -> None:
        """Start the module.  Blocks until the host sends CMD_START, then calls *fn*."""
        if self.complete_pin is not None:
            self.complete_pin.off()

        # Start the UART listener on the second core before anything else.
        _thread.start_new_thread(self._uart_thread, ())

        # Announce presence periodically until the host starts the game.
        print(f"Module {self.addr:#04x} ready, announcing on UART...")
        next_announce = ticks_ms()
        while not self.started:
            if ticks_diff(ticks_ms(), next_announce) >= 0:
                self._announce()
                next_announce = ticks_ms() + 500
            sleep(0.01)

        # Run the puzzle logic.  complete() / strike() / lose() may be called
        # from within fn() at any time; the UART thread reports the result.
        fn()

        # fn() has returned (puzzle finished); keep running so the UART thread
        # can answer further polls and handle CMD_RESET.
        while True:
            sleep(1)

    def complete(self) -> None:
        """Indicate that the player has solved this module."""
        print("Module complete.")
        if self.complete_pin is not None:
            self.complete_pin.on()
        with self._lock:
            self._status = STATUS_COMPLETE

    def strike(self) -> None:
        """Indicate that the player made a mistake."""
        print("Strike!")
        with self._lock:
            self._status = STATUS_STRIKE

    def lose(self) -> None:
        """Trigger an immediate game-over loss."""
        print("Lose triggered.")
        with self._lock:
            self._status = STATUS_LOSE
