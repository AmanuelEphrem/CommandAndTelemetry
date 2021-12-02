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
import encoder

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
			return None
		else:
			receivedPacket.decode("utf-8","strict")
			receivedJson = json.loads(receivedPacket)
			return receivedJson
	
	#Reads raw bytes to memory in a specific directory
	def _readAndStoreImageBytes(self, imgLen: int):
		self.loraRadio.ack_delay(.2) # This MIGHT let ack send better
		comArr = [None] * imgLen # Makes an empty array of the size of the length of the image. Sample(if imgLen = 12): [None, None, None, None, None, None, None, None, None, None, None, None]
		assembled = 0 # Keeps a counter of the total number of packets successfully received and put in their correct spot
		i = 0 # Keeps a counter of the number of packets received from the last 5
		recPackets = [] # Contains received packets out of the last 5 (hopefully) sent. Sample: [b(1234), b(5678), b(7890)]
		recNums = [] # Contains the location in the comArr of the received packets. Sample: [6, 7, 10]
		locPos = [] # Contains which packet out of 5 expected the received packet/num combo at the same location. Sample: [0, 1, 4]
		while assembled < imgLen: # If we have the same number (or greater) of assembled packets as we expected, end this loop.
			if i >= 5: # This is the same at at the bottom of the loop, but this just catches it if the last packet was None
				failed = self.checkLoc(locPos)
				self.loraRadio.send_with_ack(failed)
				i = 0
				recPackets = []
				recNums = []
				locPos = []
				continue
			packet = self.loraRadio.receive(with_header = True, timeout = 5) # Wait 5 for a packet
			if packet == None: # If no packet was received
				i += 1 # Increment i and restart the loop
				continue
			i += 1 # Otherwise, increment i
			num = packet[2] # Set num equal to the identifier
			print(packet)
			print(bin(num))
			pos = packet[3]
			print(packet[2:4])
			pos &= 7
			print(num)
			print(pos)
			packet = packet[4:] # Set the packet equal to the sent packet
			try:
				comArr[num] = packet # Put the packet in the location specified by the identifier
			except:
				continue
			recPackets.append(packet) # Put the received packet at the end of the recPackets list
			recNums.append(num) # Put it's corresponding number in the same location in the recNums
			locPos.append(pos) # Put it's corresponding pos in sending list in the same location in locPos
			assembled += 1 # Add 1 to assembled, since a packet was successfully received.
			if i >= 5: # If we received 5 packets since the last time we checked
				failed = self.checkLoc(locPos) # Gets the number sent back to sendImg of packets that were not received.
				self.loraRadio.send_with_ack(failed)
				i = 0 # Resets i
				recPackets = [] # Resets recPackets
				recNums = [] # Resets recNums
				locPos = [] # Resets locPos
		finArr = encoder.recombine_list(comArr)
		ans = encoder.decode_image(finArr, "newimg.png")

	def checkLoc(locPos) -> int:
		num = 0 # Set num to 0
		for j in reversed(locPos): # Go through a reversed version of locPos
			num >>= j
			num |= 1
			num <<= j
		num ^= 31
		return num
	
	#Sends the specified image over the LoRa module
	#REMEMBER: a json must first be sent to indicate that images are coming
	def _sendImage(self,  fileName:str) -> bool:
		tempArr = encoder.encode_image(fileName)
		imgArr = encoder.create_list(tempArr)
		imgLen = len(imgArr)
		incImg = {"body" : "image", "size" : imgLen}
		inc_json = json.dumps(incImg)
		self._sendJSON(inc_json)
		time.sleep(1)
		i = 0
		numSent = 0
		packToSend = [] # Empty array to hold all packets waiting to be sent
		numToSend = [] # Empty array to hold all nums corresponding to those packets
		while numSent < imgLen: # While numSent is less than the number of expected packets to send
			print("nSent", numSent)
			print("iL", imgLen)
			prevPacks = []
			prevNums = []
			while len(packToSend) < 5 and i < imgLen: # If there are more than 5 packets in packToSend OR i has exceeded the length of imgLen, don't do this
				packToSend.append(imgArr[i]) # Put a new packet on the end of the list
				numToSend.append(i) # Put it's corresponding number on the end of the other list
				i += 1 # Increment i
			cycle = len(packToSend) # Usually should be 5. However, can be less if at end of list.
			for j in range(cycle): # Just cycle through the array.
				tempPack = packToSend.pop()
				tempNum = numToSend.pop() # Remove top packet + number
				tFlag = j
				print(tempNum)
				print("j", j)
				self.loraRadio.send(tempPack, identifier = tempNum, flags = tFlag)
				prevPacks.append(tempPack)
				prevNums.append(tempNum)
				numSent += 1
			hold = self.loraRadio.receive(with_header = True, with_ack = True, timeout = 30) # Listen for a response from the other side with which packets it got. Will be an int between 0-31 inclusive.
			if(hold == None):
				continue
			hold = int.from_bytes(hold, "big")
			dropped = 0 # Which number got dropped
			while hold > 0 and dropped < len(prevPacks): # While hold is > 00000 (no dropped packets)
				if hold & 1 == 1: # Check if the bottom number of hold is 1 (aka that packet dropped)
					packToSend.append(prevPacks[dropped]) # If it is, add that packet + it's num to the packToSend
					numToSend.append(prevNums[dropped])
					numSent -= 1 # Remove 1 from numSent (since we lost a packet)
				hold >>= 1 # Rightshift hold by 1
				dropped += 1 # Increment dropped
			time.sleep(0.1)

	def addLoc(num:int, loc:int):
		num <<= 3
		num |= loc
		return num
		
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
				_readAndStoreImageBytes(payload["size"])
			else:
				_delegateData(payload)

		#send subgroupData over LoRa
		for element in list(subgroupDict.values()):
			sendingJSON = element.packageSubgroupData()
			if sendingJSON != None:
				_sendJSON(sendingJSON)
