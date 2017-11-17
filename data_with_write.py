import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
print GPIO.input(27)
print GPIO.input(17)
