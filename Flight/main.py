#This file will contain the main loop that will be on the Flight station.

import time
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from CommunicationProtocol import CommunicationProtocol
import json

def main():
	comm = CommunicationProtocol()
	sendingMessage = {"body":"test message from flight"}
	while True:
		# Do what's needed here
		jsonData = comm.communicateData(json.dumps(sendingMessage))
		if jsonData != None:
			print("body of message: "+str(jsonData["body"]))
		else:
			print("no data")
		time.sleep(0.2)

if __name__ == "__main__":
	main()
