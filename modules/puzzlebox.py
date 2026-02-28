"""A module containing the PuzzleBox module library, which is used to by modules that are designed to be used with the PuzzleBox system."""

from typing import Any, Callable

from machine import I2CTarget, Pin


class PuzzleBoxModule:
    """A class used by a module that can be used with the PuzzleBox system."""

    """The I2C target used to communicate with the host."""
    i2c: I2CTarget

    mem: bytearray

    def __init__(
        self,
        addr: int,
        *,
        id: int = 0,
        scl: int = 1,
        sda: int = 0,
    ) -> None:
        self.mem = bytearray(3)
        self.i2c = I2CTarget(
            id,
            addr,
            mem=self.mem,
            mem_addrsize=3,
            scl=Pin(scl, pull=Pin.PULL_UP),
            sda=Pin(sda, pull=Pin.PULL_UP),
        )

    def irq_handler(self, event: Any) -> None:
        """Handle an I2C event. This method should not be called manually."""
        print("I2C event occurred:", event)

    def run(self, fn: Callable[[], Any]) -> None:
        """Run the the module, with the given function as the start point of the module's execution."""
        # Set up the I2C target to call the irq_handler method when an I2C event occurs.
        self.i2c.irq(self.irq_handler)


if __name__ == "__main__":
    module = PuzzleBoxModule(0x42)
