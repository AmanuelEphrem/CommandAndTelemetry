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
import copy

class CommunicationProtocol:

	#Begins LoRa during instantiation
	def __init__(self, subgroupDictValue:dict):
		self.subgroupDict= subgroupDictValue
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
	def _sendJSON(self,jsonObject:str) -> bool:
		jsonObject.encode("utf-8","strict")
		sendingPacket = bytes(jsonObject,"utf-8")
		self.loraRadio.send(sendingPacket)
		return True
	
	#Receives JSON using LoRa
	#@return  the received JSON object as a dictionary, or None if nothing was received
	def _receiveJSON(self) -> dict:
		receivedPacket = self.loraRadio.receive()
		if receivedPacket == None:
			return None;
		else:
			receivedPacket.decode("utf-8","strict")
			receivedJson = json.loads(receivedPacket)
			return receivedJson
	
	#Reads raw bytes to memory in a specific directory
	def _readAndStoreImageBytes():
		pass
	
	#Sends the specified image over the LoRa module
	#REMEMBER: a json must first be sent to indicate that images are coming
	def _sendImage(fileName:str) -> bool:
		pass
		
	#Assigns the jsonData to the correct subgroup
	#@param  jsonData  a json dictionary 
	def _delegateData(self, jsonData:dict) -> bool:
		#if key doesn't exist
		if subgroupDict.get(jsonData["receiver"]) == None:
			return False

		subgroupDict[jsonData["receiver"]].setPayloadData(jsonData)	
		return True

	#Receives payload and distributes it to the correct subgroup and sends subgroup data over LoRa
	def eventLoop(self):
		#Receives payload
		payload = _receiveJSON()
		
		#distribute payload
		if payload != None:
			if payload["type"] == "image":
				_readAndStoreImageBytes()
			else:
				_delegateData(payload)

		#send subgroupData over LoRa
		for element in list(subgroupDict.values()):
			sendingJSON = element.packageSubgroupData()
			if sendingJSON != None:
				_sendJSON(sendingJSON)

