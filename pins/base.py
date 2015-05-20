import logging

LOGGER = logging.getLogger(__name__)

class PinInterface(object):
    def __init__(self):
        pass

    def setup(self):
        try:
            GPIO.setup(self.pin_rain_sense, GPIO.IN)
            GPIO.setup(self.pin_relay, GPIO.OUT)    
        except NameError, e:
            LOGGER.error("Failed to set GPIO directions: %s", e)

class PinInterfaceNull(object):
    def setup(self):
        LOGGER.info("Ignoring command to set up pin interface")
