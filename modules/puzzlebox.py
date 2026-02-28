"""A module containing the PuzzleBox module library, which is used to by modules that are designed to be used with the PuzzleBox system."""

try:
    from typing import Any, Callable
except ImportError:
    pass

from machine import I2CTarget, Pin, reset
from utime import sleep


class PuzzleBoxModule:
    """A class used by a module that can be used with the PuzzleBox system."""

    """The I2C target used to communicate with the host."""
    i2c: I2CTarget

    """Flag to indicate if the module has been started."""
    started: bool = False

    """The time limit for the box in seconds, as set by the host."""
    time_limit: int = 0

    """The pin used to indicate that the module is complete."""
    complete_pin: None | Pin

    mem: bytearray

    def __init__(
        self,
        addr: int,
        *,
        id: int = 1,
        scl: int = 15,
        sda: int = 14,
        complete_pin: int | None = None,
    ) -> None:
        self.complete_pin = Pin(complete_pin, Pin.OUT) if complete_pin is not None else None
        self.mem = bytearray(8)
        self.i2c = I2CTarget(
            id,
            addr,
            mem=self.mem,
            mem_addrsize=8,
            scl=Pin(scl),
            sda=Pin(sda),
        )

    def irq_handler(self, event: I2CTarget) -> None:
        """Handle an I2C event. This method should not be called manually."""
        flags = event.irq().flags()
        if flags & I2CTarget.IRQ_END_WRITE:
            if self.mem[0] == 0x01:
                print("Received command 0x01: Hello, PuzzleBox!")
                self.time_limit = int.from_bytes(self.mem[1:3], "little")
                self.started = True

            elif self.mem[0] == 0x02:
                print("Received command 0x02: Goodbye, PuzzleBox!")
                reset()

            else:
                print(f"Received unknown command: 0x{self.mem[0]:02x}")

    def run(self, fn: "Callable[[], Any]") -> None:
        """Run the the module, with the given function as the start point of the module's execution."""
        if self.complete_pin is not None:
            self.complete_pin.off()

        # Set up the I2C target to call the irq_handler method when an I2C event occurs.
        self.i2c.irq(self.irq_handler)

        # Wait for the module to be started by the host, then call the given function.
        print(f"Module listening for I2C events at {self.i2c}")
        while not self.started:
            sleep(0.1)
        fn()

        # Keep the module running until it recieves a goodbye command from the host.
        while True:
            sleep(1)

    def complete(self) -> None:
        """Indicate that the player has completed the module."""
        if self.complete_pin is not None:
            self.complete_pin.on()
        self.i2c.write(bytes([0x01]))

    def strike(self) -> None:
        """Indicate that the player has made a mistake."""
        self.i2c.write(bytes([0x02]))


if __name__ == "__main__":
    module = PuzzleBoxModule(42)
    module.run(lambda: print(f"Module started! With {module.time_limit} seconds time limit."))
