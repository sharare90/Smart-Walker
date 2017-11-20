import RPi.GPIO as GPIO
from hx711 import HX711

GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
print GPIO.input(12)

hx0 = HX711()
hx1 = HX711()
hx2 = HX711()
hx3 = HX711()

hx0.set_scale()
hx1.set_scale()
hx2.set_scale()
hx3.set_scale()

hx0.tare()
hx1.tare()
hx2.tare()
hx3.tare()

fl = hx0.get_units(10)
print fl
