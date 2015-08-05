#!/usr/bin/env python

"""UpdateGyro.py: Reads data from gyro sensor and stores it in a global variable."""

__author__ = "Vitor Bari Buccianti"
__credits__ = ["Marcin Polaczyk", "Caue Diego", "Felipe Tassoni", "Jose Rodrigo"]

__license__ = "GPL"
__version__ = "1.0"

from __future__ import print_function
from library.Gyro.L3GD20 import L3GD20

import threading
import time

from classes.RecordVideo import gyro

# ==================================
# Global Variable
# ==================================
gyro_data = {"x": 0, "y": 0, "z": 0}
file_gyro = None


class UpdateGyro(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()

        self.sensor = L3GD20(busId=1, slaveAddr=0x6b, ifLog=False, ifWriteBlock=False)

        # Gyro Pre configuration
        self.sensor.Set_PowerMode("Normal")
        self.sensor.Set_FullScale_Value("250dps")
        self.sensor.Set_AxisX_Enabled(True)
        self.sensor.Set_AxisY_Enabled(True)
        self.sensor.Set_AxisZ_Enabled(True)

        self.sensor.Init()
        self.sensor.Calibrate()

        self.last_measurement = time.time()

    def run(self):
        global file_gyro
        global gyro_data
        global gyro

        old_file = ''

        while True:
            with self.state:
                if self.paused:

                    if file_gyro:
                        file_gyro.close()

                    self.state.wait()

            if gyro["file"] == '':
                if old_file != '':
                    file_gyro.close()

                time.sleep(0.2)
            else:

                if old_file != gyro["file"]:
                    if old_file != '':
                        file_gyro.close()
                    file_gyro = open(gyro["file"], 'a')
                    old_file = gyro["file"]

                    gyro_data["x"] = 0
                    gyro_data["y"] = 0
                    gyro_data["z"] = 0

                time.sleep(0.2)

                time_gap = time.time() - self.last_measurement

                dxyz = self.sensor.Get_CalOut_Value()

                self.last_measurement = time.time()

                # sensor in different orientation
                gyro_data["x"] += dxyz[1] * time_gap
                gyro_data["y"] += -dxyz[0] * time_gap
                gyro_data["z"] += dxyz[2] * time_gap

                print("%0.3f;%0.3f;%0.3f" % (gyro_data["x"], gyro_data["y"], gyro_data["z"]), file=file_gyro)


    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()

    def pause(self):
        with self.state:
            self.paused = True