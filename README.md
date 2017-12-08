# Smart-Walker
Smart Walker is a kivy based project which aims to design user friendly and smart interface for walkers.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine 
for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Prerequisites
Use this [link](https://kivy.org/docs/installation/installation-rpi.html) 
to install the latest version of kivy on raspberry pi or follow these commands:

`sudo apt-get update`
`sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \`
`pkg-config libgl1-mesa-dev libgles2-mesa-dev \`
`python-setuptools libgstreamer1.0-dev git-core \`
`gstreamer1.0-plugins-{bad,base,good,ugly} \`
`gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \`
`Xclip`

`sudo pip install -U Cython==0.27.3`

`sudo pip install git+https://github.com/kivy/kivy.git@master`

Install BNO055 Absolute Orientation Sensor with Raspberry Pi & BeagleBone Black follow the instructions in 
[here](https://learn.adafruit.com/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black/software)

Install GPIO following the instructions 
[here](http://raspberry.io/projects/view/reading-and-writing-from-gpio-ports-from-python/)

These next instructions are used from 
[here](https://github.com/mrichardson23/rpi-kivy-screen/blob/master/README.md)

`sudo raspi-config`

and in one of the menus choose "Serial" (Enable/Disable shell and kernel messages on the serial connection) and disable it.

reboot

edit /boot/config.txt and add the line (at the bottom):
> enable_uart=1

Reboot!

## Installing

`git clone https://github.com/sharare90/Smart-Walker.git`

## Running

`cd Smart-Walker`
`python UserInterface.py`
