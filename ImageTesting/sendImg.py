import encoder
import json
from CommunicationProtocol import CommunicationProtocol
import time

def sendImg(imgname: str):
	comm = CommunicationProtocol()
	tempArr = encoder.encode_image(imgname)
	imgArr = encoder.create_list(tempArr)
	imgLen = len(imgArr)
	incImg = {"body" : "image", "size" : imgLen}
	inc_json = json.dumps(incImg)
	comm._sendJSON(inc_json)
	time.sleep(1)
	for i in range(imgLen):
		comm.sendPacket(imgArr[i], i, "bytearray")
		time.sleep(0.05)

# Figuring out how to send the pieces required, maybe?
def sendImgTest(imgname: str):
	comm = CommunicationProtocol()
	tempArr = encoder.encode_image(imgname)
	imgArr = encoder.create_list(tempArr)
	imgLen = len(imgArr)
	incImg = {"body" : "image", "size" : imgLen}
	inc_json = json.dumps(incImg)
	comm._sendJSON(inc_json)
	time.sleep(1)
	i = 0
	numSent = 0
	packToSend = [] # Empty array to hold all packets waiting to be sent
	numToSend = [] # Empty array to hold all nums corresponding to those packets
	while numSent < imgLen: # While numSent is less than the number of expected packets to send
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
			comm.sendPacket(tempPack, tempNum, "bytearray") # Send top packet + it's num.
			prevPacks.append(tempPack)
			prevNums.append(tempNum)
			numSent += 1
			time.sleep(0.05)
		hold = comm.recPacket(1000) # Listen for a response from the other side with which packets it got. Will be an int between 0-31 inclusive.
		hold = int(hold.decode("utf-8")) # !!! THIS MIGHT NOT WORK !!!
		dropped = 0 # Which number got dropped
		while hold > 0 and dropped < len(prevPacks): # While hold is > 00000 (no dropped packets)
			if hold & 1 == 1: # Check if the bottom number of hold is 1 (aka that packet dropped)
				packToSend.append(prevPacks[dropped]) # If it is, add that packet + it's num to the packToSend
				numToSend.append(prevNums[dropped])
				numSent -= 1 # Remove 1 from numSent (since we lost a packet)
			hold >>= 1 # Rightshift hold by 1
			dropped += 1 # Increment dropped



def main():
	sendImgTest("donut.png")

if __name__ == "__main__":
	main()
