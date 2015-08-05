#!/usr/bin/env python

"""RecordVideo.py: Records videos from raspicam. Split the video in a different file every 10 seconds."""

__author__ = "Vitor Bari Buccianti"
__credits__ = ["Caue Diego", "Felipe Tassoni", "Jose Rodrigo"]

__license__ = "GPL"
__version__ = "1.0"

import threading
import datetime
import picamera

# ==================================
# Global Variable
# ==================================
srt = {"file": ""}
gyro = {"file": ""}


class RecordVideo(threading.Thread):
    def __init__(self, path):
        print("RecordVideo::__init__")
        threading.Thread.__init__(self)
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()

        self.camera = None

        self.video_started = False

        self.out_path = path

    def run(self):
        global srt
        global gyro

        with picamera.PiCamera() as self.camera:

            self.camera.resolution = (1280, 720)
            self.camera.framerate = 24
            self.camera.video_stabilization = True
            self.camera.vflip = True
            self.camera.hflip = True
            self.camera.annotate_background = True
            self.camera.annotate_text = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

            while True:

                with self.state:
                    if self.paused:

                        if self.video_started:
                            self.camera.stop_recording()

                        self.state.wait()

                now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

                video_file = self.out_path + now + '.h264'
                srt["file"] = self.out_path + now + '.srt'
                gyro["file"] = self.out_path + now + '_.gyro'

                if self.video_started is False:
                    self.camera.start_recording(video_file)
                    self.video_started = True
                else:
                    self.camera.split_recording(video_file)

                start = datetime.datetime.now()
                while (datetime.datetime.now() - start).seconds < 10:
                    self.camera.annotate_text = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    self.camera.wait_recording(0.2)


    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()

    def pause(self):
        with self.state:
            self.paused = True
