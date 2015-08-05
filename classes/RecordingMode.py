#!/usr/bin/env python

"""RecordingMode.py: Starts threads for recording operating mode (camera, sensors and log files)."""

__author__ = "Vitor Bari Buccianti"
__credits__ = ["Caue Diego", "Felipe Tassoni", "Jose Rodrigo"]

__license__ = "GPL"
__version__ = "1.0"

import threading
import time

from classes.RecordVideo import RecordVideo
from classes.UpdateGps import UpdateGps
from classes.UpdateGyro import UpdateGyro
from classes.WriteLog import WriteLog
from classes.WriteSrt import WriteSrt


class RecordingMode(threading.Thread):
    def __init__(self, path):

        threading.Thread.__init__(self)
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()

        self.started = False

        self.threadRecordVideo = None
        self.threadUpdateGps = None
        self.threadUpdateGyro = None
        self.threadWriteLog = None
        self.threadWriteSrt = None

        self.out_path = path

    def run(self):

        while True:
            with self.state:
                if self.paused:
                    self.state.wait()

            time.sleep(1)

    def start_threads(self):
        self.started = True

        self.threadUpdateGps = UpdateGps()
        self.threadUpdateGps.resume()
        self.threadUpdateGps.start()

        self.threadUpdateGyro = UpdateGyro()
        self.threadUpdateGyro.resume()
        self.threadUpdateGyro.start()

        self.threadRecordVideo = RecordVideo(self.out_path)
        self.threadRecordVideo.resume()
        self.threadRecordVideo.start()

        self.threadWriteSrt = WriteSrt()
        self.threadWriteSrt.resume()
        self.threadWriteSrt.start()

        self.threadWriteLog = WriteLog(self.out_path)
        self.threadWriteLog.resume()
        self.threadWriteLog.start()

    def resume(self, blinkLed, start=True):
        if start and not self.started:
            self.start_threads()
        elif start and self.started:
            self.threadRecordVideo.resume()
            self.threadWriteLog.resume()
            self.threadWriteSrt.resume()
            self.threadUpdateGyro.resume()
            self.threadUpdateGps.resume()

        with self.state:
            self.paused = False
            self.state.notify()

        if blinkLed:
            blinkLed.set_interval(3)

    def pause(self):

        with self.state:
            self.paused = True

        if self.started:
            self.threadRecordVideo.pause()
            self.threadWriteLog.pause()
            self.threadWriteSrt.pause()
            self.threadUpdateGyro.pause()
            self.threadUpdateGps.pause()
            self.threadCleanFiles.pause()

