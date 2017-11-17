import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

for i in range(40):
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    print GPIO.input(i)
