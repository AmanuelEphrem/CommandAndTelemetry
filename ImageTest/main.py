import time
import sys
sys.path.append("..") # Adds higher directory to python so CommunicationProtocol can be accessed.
import CommunicationProtocol
import json

# Test to receive IMAGES only!!
def main():
	comm  = CommunicationProtocol()
	sendingMessage = {"body" : "dud message"}	
	while True:
		receivedData = comm.communicateData(json.dumps(sendingMessage))
		if receivedData != None:
			print("Data received: "+str(receivedData["image"]))
		else:
			print("no data")

if __name__ == "__main__":
	main()
