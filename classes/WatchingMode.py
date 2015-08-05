#!/usr/bin/env python

"""WatchingMode.py: Loops through recorded videos and cube simulations."""

__author__ = "Vitor Bari Buccianti"
__credits__ = ["Caue Diego", "Felipe Tassoni", "Jose Rodrigo"]

__license__ = "GPL"
__version__ = "1.0"

import threading
import time
import os

from classes.GyroCube import Simulation


class WatchingMode(threading.Thread):
    def __init__(self, out_path):
        threading.Thread.__init__(self)
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()

        self.started = False

        self.out_path = out_path

    def run(self):
        while True:
            with self.state:
                if self.paused:

                    if self.started:
                        os.system("sudo killall omxplayer")

                    self.state.wait()

            time.sleep(2)

            lst = os.listdir(self.out_path)
            lst.sort()

            for file in lst:

                if self.paused:
                    break

                if file.endswith(".h264"):
                    os.system("omxplayer " + self.out_path + file)

                if file.endswith(".gyro"):
                    Simulation().run(self.out_path + file)

            time.sleep(5)

    def resume(self, blinkLed):
        with self.state:
            self.paused = False
            self.state.notify()

        self.started = True

        if blinkLed:
            blinkLed.set_interval(1)

    def pause(self):
        with self.state:
            self.paused = True
			