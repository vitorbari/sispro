#!/usr/bin/env python

"""UpdateGps.py: Reads data from gps and stores it in a global variable."""

__author__ = "Vitor Bari Buccianti"
__credits__ = ["Caue Diego", "Felipe Tassoni", "Jose Rodrigo"]

__license__ = "GPL"
__version__ = "1.0"


from gps import *

import threading

# ==================================
# Global Variable
# ==================================
gps_data = {"status": 0, "lat": 0, "long": 0, "speed": 0, "alt": 0}


class UpdateGps(threading.Thread):
    def __init__(self):

        threading.Thread.__init__(self)
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()

        self.gpsd = gps(mode=WATCH_ENABLE)

    def run(self):
        global gps_data

        while True:
            with self.state:
                if self.paused:
                    self.state.wait()

            self.gpsd.next()

            gps_data["status"] = self.gpsd.fix.mode  # "ZERO", "NO_FIX", "2D", "3D"
            gps_data["speed"] = self.gpsd.fix.speed * 1.852  # knots to km/h - Is it really in knots?
            gps_data["lat"] = self.gpsd.fix.latitude
            gps_data["long"] = self.gpsd.fix.longitude
            gps_data["alt"] = self.gpsd.fix.altitude
            gps_data["climb"] = self.gpsd.fix.climb
            gps_data["satellites"] = self.gpsd.satellites_used

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()

    def pause(self):
        with self.state:
            self.paused = True
