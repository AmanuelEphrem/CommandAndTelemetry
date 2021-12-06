import sys
sys.path.append("..") # Adds higher directory to python modules path.
import CommunicationProtocol
import SubgroupClass
import ThreadingClass
import Threading
import socket
def main():
	groundStation = SubgroupClass("groundStation",56783)
	dictOfSubgroup = {"groundStation":groundStation}	
	commProtocol = CommunicationProtocol(dictOfSubgroup)
		
	# This is super ugly, but it allows us to get the local ip of the pi and use that as the running IP for the socket.
	hostname = socket.gethostname()
	IP = socket.gethostbyname(hostname)
	#begin background thread (passing in groundStation as a reference)
	x = threading.Thread(target=ThreadingClass.thrSocket,args=(dictOfSubgroups, IP),daemon=True)
	x.start()
	
	keepConnectionAlive = True
	while keepConnectionAlive:
		#Sends and receives messages over LoRa
		commProtocol.eventLoop()
		print("event loop running")
	

if __name__ == "__main__":
	main()
