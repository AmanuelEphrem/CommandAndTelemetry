# The Communication Protocol to communicate with the Flight Unit
# This is a test file that will establish communication with the flight unit and print out the "conversation" in stdout

# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x


#Setup Lora
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
loraRadio = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
loraRadio.tx_power = 23
prev_packet = None

while True:
	packet = None
	# check for packet rx
	packet = loraRadio.receive()
	
	if packet == None:
		print("No Data Received")
	
	else:
		prev_packet = packet
		packet_text = str(prev_packet, "utf-8")
		print(packet_text)
		time.sleep(1)
	
 	time.sleep(0.1)









