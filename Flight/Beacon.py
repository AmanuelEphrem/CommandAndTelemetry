import time

#imports for beacon light
import RPi.GPIO as GPIO

# Beacon set up
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT,initial=GPIO.LOW)

#runs Beacon blinking
while True:
	GPIO.output(17,GPIO.HIGH)
	time.sleep(.5)
	GPIO.output(17,GPIO.LOW)
	time.sleep(.5)
