#The CommunicationProtocol Class is how the Ground and Flight stations will communicate over the LoRa module. 
#Communication over the LoRa module should occur within this class ONLY!

#Import libraries needed for LoRa module
import time
import busio #import blinka libraries
from digitalio import DigitalInOut, Direction, Pull
import board # this is found only on raspberry pi
#import adafruit_ssd1306
import adafruit_rfm9x #import Rfm9x
import json

class CommunicationProtocol:

	#Begins LoRa during instantiation
	def __init__(self):
		self._loraSetup()

	#Setup for the LoRa module
	def _loraSetup(self) -> bool:
		CS = DigitalInOut(board.CE1)
		RESET = DigitalInOut(board.D25)
		spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
		self.loraRadio = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
		self.loraRadio.tx_power = 23
		return True
	
	#Sends JSON using LoRa
	#@param  jsonObject  a JSON string to send
	#@return  True if sending is successful, False otherwise
	def _sendJSON(self,jsonObject) -> bool:
		jsonObject.encode("utf-8","strict")
		sendingPacket = bytes(jsonObject,"utf-8")
		self.loraRadio.send(sendingPacket)
		return True
	#@return  the received JSON object as a dictionary, or None if nothing was received
	def _receiveJSON(self) -> dict:
		receivedPacket = self.loraRadio.receive()
		if receivedPacket == None:
			return None;
		else:
			receivedPacket.decode("utf-8","strict")
			receivedJson = json.loads(receivedPacket)
			return receivedJson
		
	#Attempts to send, receive, and return received json
	#@param  jsonToSend  a JSON string to send
	#@return  the received JSON object as a dictionary, or None if nothing was received
	def communicateData(self, jsonToSend) -> dict:
		self._sendJSON(jsonToSend)
		return self._receiveJSON()
