import logging
import json
import sys
import time
from Adafruit_BNO055 import BNO055
import RPi.GPIO as GPIO
from hx711 import HX711


#GPIO SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# Create a VL53L0X prox object

# Create a BNO055 IMU object
bno = BNO055.BNO055(serial_port='/dev/ttyS0', rst=23)


#------------------------------------

#INITIALIZATION & CALIBRATION

#identify ADCs & assign pins
        
hx0 = HX711(27, 17, 128)
hx1 = HX711(10, 22, 128)
hx2 = HX711(11, 9, 128)
hx3 = HX711(26, 13, 128)

#Balance Scale and Tare
hx0.set_scale(7050)
hx1.set_scale(7050)
hx2.set_scale(7050)
hx3.set_scale(7050)

hx0.tare()
hx1.tare()
hx2.tare()
hx3.tare()

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

print('Press Ctrl-C to quit...')


# Start ranging for proximity sensor


#Create new data file
with open('Raw_Data/count.txt', "r+") as fp:
    count = fp.read()
    count = str(int(count) + 1)
    fp.close
with open('Raw_Data/count.txt', "w+") as fp:
    fp.write(count)
    fp.close
    
filename = "Raw_Data/" + count + " - Walker Data Record.txt"
fp = open(filename, "w+")

#------------------------------------


#Merged Measurement Loop

while True:
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno.get_calibration_status()

    val0 = hx0.get_units(1)
    offset = max(1,min(80,int(val0+40)))
    val1 = hx1.get_units(1)
    offset = max(1,min(80,int(val1+40)))
    val2 = hx2.get_units(1)
    offset = max(1,min(80,int(val2+40)))
    val3 = hx3.get_units(1)
    offset = max(1,min(80,int(val3+40)))
#    print ("{0: 4.3f}".format(val0),
#           "{0: 4.3f}".format(val1),
#           "{0: 4.3f}".format(val2),
#           "{0: 4.3f}".format(val3));
    
    # Read the distance from the proximity sensor

    #Write Raw Data to File


tof.stop_ranging()

