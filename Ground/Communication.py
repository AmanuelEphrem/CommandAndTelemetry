# The Communication Protocol to communicate with ground control
# This is a test file that will establish communication with ground control and print out the "conversation" in stdout

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

def loraSetup():
	#Setup Lora
	CS = DigitalInOut(board.CE1)
	RESET = DigitalInOut(board.D25)
	spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
	loraRadio = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
	loraRadio.tx_power = 23
	prev_packet = None

# Reads received packets and prints them to stdout. If no packet is available "No Data Received is printed"
def receiveMessage():
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

# Sends indicated message via lora chip
def sendMessage(message):
	sendingPacket = bytes(message)
	loraRadio.send(sendingPacket)


def main():
	# lora chip setup
	loraSetup();

	# Main Communication loop
	while True:
		receiveMessage()
		time.sleep(0.1)
		sendMessage("Sending from ground to flight")
		time.sleep(0.1)


# Runs the main function only if called from terminal
if __name__ == __main__:
	main();


