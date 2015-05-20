import gv
import logging
import pins.base

LOGGER = logging.getLogger(__name__)

class PinInterfaceShiftRegister(pins.base.PinInterface):
    def setup(self):
        super(PinInterfaceShiftRegister, self).__init__()
        gv.GPIO.setup(self.pin_sr_noe, gv.GPIO.OUT)
        gv.GPIO.output(self.pin_sr_noe, gv.GPIO.HIGH)
        gv.GPIO.setup(self.pin_sr_clk, gv.GPIO.OUT)
        gv.GPIO.output(self.pin_sr_clk, gv.GPIO.LOW)
        gv.GPIO.setup(self.pin_sr_dat, gv.GPIO.OUT)
        gv.GPIO.output(self.pin_sr_dat, gv.GPIO.LOW)
        gv.GPIO.setup(self.pin_sr_lat, gv.GPIO.OUT)
        gv.GPIO.output(self.pin_sr_lat, gv.GPIO.LOW)

    def disable_shift_register_output(self):
        """Disable output from shift register."""
        try:
            gv.GPIO.output(self.pin_sr_noe, gv.GPIO.HIGH)
        except Exception as e:
            LOGGER.error("Failed to disable shift register output: %s", e)

    def enable_shift_register_output(self):
        """Enable output from shift register."""
        try:
            gv.GPIO.output(self.pin_sr_noe, gv.GPIO.LOW)
        except Exception as e:
            LOGGER.error("Failed to disable shift register output: %s", e)

    def set_shift_register(self, srvals):
        """Set the state of each output pin on the shift register from the srvals list."""
        try:
            gv.GPIO.output(self.pin_sr_clk, gv.GPIO.LOW)
            gv.GPIO.output(self.pin_sr_lat, gv.GPIO.LOW)
            for s in range(gv.sd['nst']):
                gv.GPIO.output(self.pin_sr_clk, gv.GPIO.LOW)
                if srvals[gv.sd['nst']-1-s]:
                    gv.GPIO.output(self.pin_sr_dat, gv.GPIO.HIGH)
                else:
                    gv.GPIO.output(self.pin_sr_dat, gv.GPIO.LOW)
                gv.GPIO.output(self.pin_sr_clk, gv.GPIO.HIGH)
            gv.GPIO.output(self.pin_sr_lat, gv.GPIO.HIGH)
        except Exception as e:
            LOGGER.exception("Failed to set shift register")

    def set_output(self, register_values):
        LOGGER.debug("Setting output to %s", register_values)
        self.disable_shift_register_output()
        self.set_shift_register(register_values)  
        self.enable_shift_register_output()

class PinInterfacePi(PinInterfaceShiftRegister):
    def __init__(self):
        # IO channels are identified by header connector pin numbers. Pin numbers are always the same regardless of Raspberry Pi board revision.
        self.pin_rain_sense = 8
        self.pin_relay = 10
        self.pin_sr_dat = 13
        self.pin_sr_clk = 7
        self.pin_sr_noe = 11
        self.pin_sr_lat = 15
        gv.GPIO.setmode(gv.GPIO.BOARD)
        super(PinInterfacePi, self).__init__()

class PinInterfaceBeagleBone(PinInterfaceShiftRegister):
    def __init__(self):
        self.pin_rain_sense = "P9_15"
        self.pin_relay = "P9_16"
        self.pin_sr_dat = "P9_11"
        self.pin_sr_clk = "P9_13"
        self.pin_sr_noe = "P9_14"
        self.pin_sr_lat = "P9_12"
        super(PinInterfaceBeagleBone, self).__init__()

