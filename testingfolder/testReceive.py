# The Communication Protocol to communicate with ground control
# This is a test file that will establish communication with ground control and print out the "conversation" in stdout

# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board # this is found only on raspberry pi
# Import the SSD1306 module.
#import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x
import encoder

def loraSetup():
	global loraRadio
	#Setup Lora
	CS = DigitalInOut(board.CE1)
	RESET = DigitalInOut(board.D25)
	spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
	loraRadio = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
	loraRadio.tx_power = 23
	prev_packet = None

# Reads received packets and prints them to stdout. If no packet is available "No Data Received is printed"
def receiveMessage():
	packet = None
	# check for packet rx
	packet = loraRadio.receive(with_header = True)
	if packet == None:
		print("No Data Received")
		return None
	else:
		iden = packet[2]
		prev_packet = packet[4]
		if prev_packet == "IMAGE INCOMING":
			recieveImage(iden)
		return prev_packet

# Sends indicated message via lora chip
def sendMessage(message, numSent):
	sendingPacket = message
	loraRadio.send(sendingPacket, identifier = numSent)

def sendImage(img_name):
	arr = encoder.encode_image(img_name)
	arr = encoder.create_list(arr)
	leng = len(arr)
	sendMessage(bytes.("IMAGE INCOMING", leng))
	for i in range(leng):
		sendMessage(arr[i], i)

def recieveImage(length):
	tempArr = [None] * length
	for i in range(length):
		packet = loraRadio.recieve(with_header = True)
		tempArr[packet[2]] = packet[4]
	fin_arr = encoder.recombine_list(tempArr)
	encoder.decode_image(fin_arr, "newimg.png") # Placeholder name

def main():
	# lora chip setup
	loraSetup();

	# Main Communication loop
	while True:
		recieveMessage()
		time.sleep(0.1)


# Runs the main function only if called from terminal
if __name__ == "__main__":
	print("main method here")	
	main();
