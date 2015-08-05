#!/usr/bin/env python

"""Util.py: Contains helper functions."""

__author__ = "Vitor Bari Buccianti"
__credits__ = ["Caue Diego", "Felipe Tassoni", "Jose Rodrigo"]

__license__ = "GPL"
__version__ = "1.0"

import RPi.GPIO as GPIO
import os
import errno


class Util(object):
    @staticmethod
    def make_sure_path_exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    @staticmethod
    def cleanup_stop():
        GPIO.cleanup()
		