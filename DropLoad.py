import time

import RPi.GPIO as GPIO

target = 20 #change as needed

# load set up
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(target,GPIO.OUT,initial=GPIO.LOW) 

#drops the load
def dropLoad():
	GPIO.output(target,GPIO.HIGH)
	time.sleep(.5)
	GPIO.output(target,GPIO.LOW)
	time.sleep(.5)

#99% of this was just stolen from the beacon
