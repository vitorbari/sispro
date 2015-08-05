# SISPRO

SISPRO is a Raspberry Pi / Python based GPS & video tracking system. 

##### Table of Contents  
[Introduction](#introduction)  
[Parts](#parts)  
[Schematics](#schematics)  
[Installation](#installation)  
[Roadmap](#roadmap)  
[References](#references)  
[Contributing](#contributing)  

## Introduction

SISPRO is a tracking system for Raspberry PI which uses a [Raspberry Camera Module](https://www.raspberrypi.org/products/camera-module/) and a [Adafruit Ultimate GPS Breakout](http://www.adafruit.com/product/746). It records videos over multiple files and writes .srt (subtitle) files with GPS data (Lat / Long; Km/h; etc). The system also writes a log file with lots of information.

It has 2 operating modes:

* **Recording mode**: Records the videos and text files (srt and log)
* **Watching mode**: Plays the recorded videos in loop 

It has been only tested on a Raspberry Pi Model B running [Raspbian](https://www.raspbian.org/).

## Parts

* [Raspberry Pi](https://www.raspberrypi.org/products/model-b/)
* [Raspberry Camera Module](https://www.raspberrypi.org/products/camera-module/)
* [Adafruit Ultimate GPS Breakout](http://www.adafruit.com/product/746)
* 3 LEDs (+ resistors)
* 3 Switchs (Normally Open)

## Schematics

![Sispro Schematics](schematics/sispro.schema.png?raw=true)

## Installation

Assuming you have Raspbian installed and internet connection:

### Pre Installation Steps

1. Firmware Update
 
 ```bash
 $ sudo rpi-update
 ```
2. Update the list of available packages and their versions
 
 ```bash
 $ sudo apt-get update
 ```
3. Install newer versions of the packages you have
 
 ```bash
 $ sudo apt-get upgrade
 ```

### Installation Steps
1. Enable Camera Module

 ```bash
 $ sudo raspi-config
 ```
2. Install dependencies

 ```bash
 $ sudo apt-get install python-picamera python3-picamera python-rpi.gpio gpsd gpsd-clients python-gps python-smbus
 ```
3. GPS Setup
  
  Edit /boot/cmdline.txt - When the Pi is booting all the debug messages are sent to the serial port. This can be useful for some purposes but we need to turn this off to free the port for our own use.
   ```bash
   $ sudo nano /boot/cmdline.txt
   ```
   And change:  
   `dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait`  
   to:  
   `dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait` 
  
  Edit /etc/inittab - To disable the login feature we can run the following command to edit the inittab system file
   ```bash
   $ sudo nano /etc/inittab
   ```
   And change:  
   `T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100`  
   to:  
   `#T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100`
4. Grab the source code

 ```bash
 $ cd ~  
 $ wget https://github.com/vitorbari/sispro.git
 ```

### Optional Post Installation Steps
1. Camera Module Test  

 ```bash
 $ raspistill -o image.jpg
 ```
2. GPS Module Test  

 ```bash
 $ cgps -s
 ```
2. Start Sispro at boot time 
(TODO)
3. Enable Auto Login

 ```bash
 $ sudo nano /etc/inittab
 ```

 And change:  
 `1:2345:respawn:/sbin/getty 115200 tty1`  
 to:  
 `#1:2345:respawn:/sbin/getty 115200 tty1`

 Under that line add:  
 `1:2345:respawn:/bin/login -f pi tty1 </dev/tty1 >/dev/tty1 2>&1`
4. Enable HDMI Hotplug  
 ```bash
 $ sudo nano /boot/config.txt
 ```

 And change:  
 `hdmi_force_hotplug=0`  
 to:  
 `hdmi_force_hotplug=1`

## Roadmap

* Add RTC
* Add Inertial sensors
* Add ODB2 Connectivity

## References

* [http://picamera.readthedocs.org/en/release-1.8/recipes1.html#recording-over-multiple-files](http://picamera.readthedocs.org/en/release-1.8/recipes1.html#recording-over-multiple-files)
* [https://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi?view=all](https://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi?view=all)
* [https://embeddedcode.wordpress.com/2013/10/18/adding-a-shutdown-button-to-the-raspberry-pi/](https://embeddedcode.wordpress.com/2013/10/18/adding-a-shutdown-button-to-the-raspberry-pi/)

## Contributing

If you would like help implementing a new feature or fixing a bug, fork the repo and submit a pull request!