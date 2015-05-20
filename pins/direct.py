import gv
import logging
import pins.base

LOGGER = logging.getLogger(__name__)

class PinInterfaceDirect(pins.base.PinInterface):
    def setup(self):
        self.pins = [11, 13, 15, 19, 21, 23,   8, 10, 16, 18, 22, 24]
        gv.GPIO.setmode(gv.GPIO.BOARD)
        for pin in self.pins:
            gv.GPIO.setup(pin, gv.GPIO.OUT)
            gv.GPIO.output(pin, False)

    def shutdown(self):
        gv.GPIO.cleanup()

    def set_output(self, register_values):
        for i, is_high in enumerate(register_values):
            try:
                pin = self.pins[i]
                gv.GPIO.output(pin, is_high)
                LOGGER.debug("Set valve %s (pin %s) to %s", i, pin, is_high)
            except IndexError:
                pass
