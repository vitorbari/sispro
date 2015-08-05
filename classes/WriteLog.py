#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""WriteLog.py: Writes a csv file with the data read from sensors."""

__author__ = "Vitor Bari Buccianti"
__credits__ = ["Caue Diego", "Felipe Tassoni", "Jose Rodrigo"]

__license__ = "GPL"
__version__ = "1.0"

from __future__ import print_function

import threading
import datetime
import time
import csv

from classes.UpdateGps import gps_data
from classes.UpdateGyro import gyro_data

# ==================================
# Global Variable
# ==================================
file_log = None


class WriteLog(threading.Thread):
    def __init__(self, path):

        threading.Thread.__init__(self)
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()

        self.out_path = path

    def run(self):
        global file_log
        global gps_data
        global gyro_data

        now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = self.out_path + now + '_log.csv'

        with open(file_name, 'w') as file_log:

            csvwriter = csv.writer(file_log, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

            # Header
            csvwriter.writerow(['Date Time', 'X axis', 'Y axis', 'Z axis', 'Lat', 'Long', 'Speed (Km/h)',
                                'Altitude (m)', 'Climb (m/s)', 'Number of Satellites', 'Google Maps Link'])

            time.sleep(1)

            while True:
                with self.state:
                    if self.paused:

                        if file_log:
                            file_log.flush()

                        self.state.wait()

                if gps_data["status"] > 1:
                    csvwriter.writerow(
                        [datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'), "{0:.2f}".format(gyro_data["x"]),
                         "{0:.2f}".format(gyro_data["y"]), "{0:.2f}".format(gyro_data["z"]),
                         "{0:.7f}".format(gps_data["lat"]), "{0:.7f}".format(gps_data["long"]), gps_data["speed"],
                         gps_data["alt"], gps_data["climb"], gps_data["satellites"],
                         self.get_gmaps_url(gps_data["lat"], gps_data["long"])])
                else:
                    csvwriter.writerow(
                        [datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'), "{0:.2f}".format(gyro_data["x"]),
                         "{0:.2f}".format(gyro_data["y"]), "{0:.2f}".format(gyro_data["z"]), "", "", "", "", "", ""])

                time.sleep(1)

    def deg_to_dms(self, deg):
        d = int(deg)
        md = abs(deg - d) * 60
        m = int(md)
        sd = (md - m) * 60
        return "%0.0f°%0.0f'%0.1f\"" % (d, m, sd)

    def get_gmaps_url(self, lat, long):
        return "https://www.google.com.br/maps/place/" + self.deg_to_dms(lat) + "+" + self.deg_to_dms(long) + "/@" + (
        "%0.6f" % lat) + "," + ("%0.6f" % long)

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()

    def pause(self):
        with self.state:
            self.paused = True
