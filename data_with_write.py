import logging
import json
import sys
import time
from Adafruit_BNO055 import BNO055
import RPi.GPIO as GPIO


#GPIO SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# Create a VL53L0X prox object

# Create a BNO055 IMU object
bno = BNO055.BNO055(serial_port='/dev/ttyS0', rst=23)


#------------------------------------

#INITIALIZATION & CALIBRATION

#identify ADCs & assign pins


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


#------------------------------------


#Merged Measurement Loop

#    print ("{0: 4.3f}".format(val0),
#           "{0: 4.3f}".format(val1),
#           "{0: 4.3f}".format(val2),
#           "{0: 4.3f}".format(val3));
    
    # Read the distance from the proximity sensor

    #Write Raw Data to File




