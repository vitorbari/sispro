#!/usr/bin/env python
"""WriteSrt.py: Writes a srt (subtitles) file with the data read from sensors."""

__author__ = "Vitor Bari Buccianti"
__credits__ = ["Caue Diego", "Felipe Tassoni", "Jose Rodrigo"]

__license__ = "GPL"
__version__ = "1.0"

from __future__ import print_function
from datetime import timedelta

import threading
import time

from classes.UpdateGps import gps_data
from classes.RecordVideo import srt

# ==================================
# Global Variable
# ==================================
file_srt = None


class WriteSrt(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()

    def run(self):
        global file_srt
        global gps_data
        global srt

        duration_sec = 0.2

        old_file = ''

        while True:
            with self.state:
                if self.paused:

                    if file_srt:
                        file_srt.close()

                    self.state.wait()

            if srt["file"] == '':
                if old_file != '':
                    file_srt.close()

                time.sleep(0.2)
            else:

                if old_file != srt["file"]:
                    if old_file != '':
                        file_srt.close()
                    file_srt = open(srt["file"], 'a')
                    old_file = srt["file"]
                    srt_i = 1

                    t = timedelta()

                video_tempo = str(t)[:7] + "," + `t.microseconds / 1000`
                t = t + timedelta(seconds=duration_sec)
                video_tempo = video_tempo + " --> " + str(t)[:7] + "," + `t.microseconds / 1000`

                print(srt_i, file=file_srt)  # Subtitle index
                print(video_tempo, file=file_srt)  # Time

                if gps_data["status"] > 1:
                    print("%0.7f %0.7f\n%0.2fKm/h Alt:%0.2fm" % (gps_data["lat"], gps_data["long"], gps_data["speed"], gps_data["alt"]), file=file_srt)
                else:
                    print("(GPS NO-FIX)", file=file_srt)

                srt_i += 1

                time.sleep(duration_sec)


    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()

    def pause(self):
        with self.state:
            self.paused = True