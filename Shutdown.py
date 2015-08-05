#!/usr/bin/env python

"""Shutdown.py: This script will wait for a button to be pressed and then shutdown or reboot the Raspberry Pi"""

__author__ = "Vitor Bari Buccianti"
__credits__ = ["FLIPDOT - http://spaceblogs.org/", "Caue Diego", "Felipe Tassoni", "Jose Rodrigo"]

__license__ = "GPL"
__version__ = "1.0"

import RPi.GPIO as GPIO
import time
import os
import sys

pin_led_power = 16
pin_shutdown_switch = 15
pin_reset_switch = 13

GPIO.setmode(GPIO.BOARD)

GPIO.setup(pin_led_power, GPIO.OUT)
GPIO.setup(pin_shutdown_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_reset_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ==================================
# Global variables
# ==================================
run = 1

def int_shutdown(channel):
    """
    shutdown Raspberry Pi
    :param channel:
    """
    global run
    run = 0
    os.system("sudo shutdown -h now")


def int_reset(channel):
    """
    reset Raspberry Pi
    :param channel:
    """
    global run
    run = 0
    os.system("sudo reboot")


try:

    GPIO.add_event_detect(pin_shutdown_switch, GPIO.FALLING, callback=int_shutdown, bouncetime=2000)
    GPIO.add_event_detect(pin_reset_switch, GPIO.FALLING, callback=int_reset, bouncetime=2000)

    while 1:
        if run:
            # blinks led every 1.5 seconds
            GPIO.output(pin_led_power, True)
            time.sleep(0.1)

            GPIO.output(pin_led_power, False)
            time.sleep(1.5)

        else:
            # keeps led on until the end of the process
            GPIO.output(pin_led_power, True)
            time.sleep(1)


except KeyboardInterrupt:

    GPIO.cleanup()

    sys.exit(0)

else:
    raise


