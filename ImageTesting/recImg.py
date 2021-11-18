import encoder
import json
import busio 
from digitalio import DigitalInOut, Direction, Pull
import board # this is found only on raspberry pi
import adafruit_rfm9x 
from CommunicationProtocol import CommunicationProtocol

# THIS WILL BE REMOVED LATER - ITS IMPORTANT NOW FOR TESTING
def loraSetup(): # POSSIBLE ERROR: THIS MAY NOT WORK WITH COMMUNICATION PROTOCOL.
	global loraRadio
	CS = DigitalInOut(board.CE1)
	RESET = DigitalInOut(board.D25)
	spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
	loraRadio = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
	loraRadio.tx_power = 23

# def receiveMessage():
# 	packet = None
# 	# check for packet rx
# 	packet = loraRadio.receive(with_header = True)
# 	if packet == None:
# 		print("No Data Received")
# 		return None
# 	else:
# 		iden = packet[2]
# 		prev_packet = packet[4].decode("utf-8")
# 		if prev_packet == "IMAGE INCOMING":
# 			recImg(iden)
# 		return prev_packet

def recImg(imgLen: int):
    comArr = [None] * imgLen
    for i in range(imgLen): # TODO: Update this implementation to deal with lost/dropped packets.
        packet = loraRadio.receive(with_header = True)
        comArr[packet[2]] = packet[4] # packet[2] should be the location in the array the packet should go. packet[4] should be the bytearray.
    finArr = encoder.recombine_list(comArr)
    ans = encoder.decode_image(finArr, "newimg.png") # Placeholder name

def main():
    comm = CommunicationProtocol()
    while True:
        ans = comm.receiveJSON()
	if ans['base'] == 'image':
		recImg(ans['size'])
	
