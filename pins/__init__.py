# -*- coding: utf-8 -*-
import gv
import logging
import pins.shift_register

LOGGER = logging.getLogger(__name__)

from gv import GPIO
from blinker import signal

zone_change = signal('zone_change')

def check_rain():
    try:
        if gv.sd['rst'] == 1:  # Rain sensor type normally open (default)
            if not GPIO.input(pin_rain_sense):  # Rain detected
                gv.sd['rs'] = 1
            else:
                gv.sd['rs'] = 0
        elif gv.sd['rst'] == 0:  # Rain sensor type normally closed
            if GPIO.input(pin_rain_sense):  # Rain detected
                gv.sd['rs'] = 1
            else:
                gv.sd['rs'] = 0
    except NameError as e:
        LOGGER.error("Failed to check rain: %s", e)

def setup():
    try:
        GPIO.setwarnings(False)
    except Exception as e:
        LOGGER.error("Failed to disable GPIO warnings: %s", e)

    if gv.platform == 'pi':  # If this will run on Raspberry Pi:
        setup.interface = pins.shift_register.PinInterfacePi()
    elif gv.platform == 'bo':  # If this will run on Beagle Bone Black:
        setup.interface = pins.shift_register.PinInterfaceBeagleBone()
    else:
        LOGGER.warning('platform is not set, unable to create interface')
        setup.interface = pins.base.PinInterfaceNull()

    setup.interface.setup()
setup.interface = None

def set_output():
    """Activate triacs according to shift register state."""
    # gv.srvals stores shift register state
    setup.interface.set_output(gv.srvals)
    zone_change.send()
