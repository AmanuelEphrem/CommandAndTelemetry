#This file will contain the main loop that will be on the Flight station.

import time
import sys
sys.path.append("..") # Adds higher directory to python modules path.
import CommunicationProtocol

def main():
	comm = CommunicationProtocol()
	sendingMessage = {"body":"test message from flight"}
	while True:
		# Do what's needed here
		comm.communicateData(json.dumps(sendingMessage))
		time.sleep(0.2)

if __name__ == "__main__":
	main()
