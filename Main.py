#!/usr/bin/env python

"""Main.py: This script switches between the two operating modes (recording and watching)."""

__author__ = "Vitor Bari Buccianti"
__credits__ = ["Caue Diego", "Felipe Tassoni", "Jose Rodrigo"]

__license__ = "GPL"
__version__ = "1.0"

from __future__ import print_function

import RPi.GPIO as GPIO
import time
import datetime

from classes.BlinkLed import BlinkLed
from classes.RecordingMode import RecordingMode
from classes.Util import Util
from classes.WatchingMode import WatchingMode

# ==================================
# Threads global variables
# ==================================
from classes.WriteLog import file_log
from classes.WriteSrt import file_srt


def set_mode_interrupt(channel):
    """
    switch between operating modes
    :param channel:
    """
    global pin_record_switch
    global operating_mode

    time.sleep(0.5)

    switch_state = GPIO.input(pin_record_switch)

    if switch_state == 1:

        if operating_mode == 1:
            ThreadRecordingMode.pause()

        ThreadWatchingMode.resume(ThreadBlinkLed)
        operating_mode = 2

    elif switch_state == 0:

        if operating_mode == 2:
            ThreadWatchingMode.pause()

        ThreadRecordingMode.resume(ThreadBlinkLed)
        operating_mode = 1


# ==================================
# Pins Setup
# ==================================

pin_main_led = 7
pin_record_switch = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Output
GPIO.setup(pin_main_led, GPIO.OUT)

# Input
GPIO.setup(pin_record_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)



# ==================================
# Main
# ==================================
try:

    # operating mode switch
    GPIO.add_event_detect(pin_record_switch, GPIO.BOTH, callback=set_mode_interrupt, bouncetime=2000)

    out_path = '/home/pi/sispro/out/' + datetime.datetime.now().strftime('%Y-%m-%d') + '/'
    Util.make_sure_path_exists(out_path)

    ThreadRecordingMode = RecordingMode(out_path)
    ThreadRecordingMode.start()

    ThreadWatchingMode = WatchingMode(out_path)
    ThreadWatchingMode.start()

    ThreadBlinkLed = BlinkLed(pin_main_led)
    ThreadBlinkLed.start()

    # Starts current operating mode
    operating_mode = 0
    set_mode_interrupt(0)

    while True:
        time.sleep(1)


except:

    if operating_mode == 1:
        ThreadRecordingMode.pause()

    if operating_mode == 2:
        ThreadWatchingMode.pause()

    if file_log:
        file_log.close()

    if file_srt:
        file_srt.close()

    ThreadBlinkLed.set_interval(0.1)
    time.sleep(5)
    ThreadBlinkLed.pause()

    Util.cleanup_stop()

    # sys.exit(0)

    raise
