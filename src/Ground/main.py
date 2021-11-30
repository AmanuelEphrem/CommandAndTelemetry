import sys
sys.path.append("..") # Adds higher directory to python modules path.
import CommunicationProtocol
import SubgroupClass
import ThreadingClass
import Threading
def main():
	groundStation = SubgroupClass("groundStation",56783)
	dictOfSubgroup = {"groundStation":groundStation}	
	commProtocol = CommunicationProtocol(dictOfSubgroup)
		
	#begin background thread (passing in groundStation as a reference)
	x = threading.Thread(target=ThreadingClass.thrSocket,args=(dictOfSubgroups),daemon=True)
	x.start()
	
	keepConnectionAlive = True
	while keepConnectionAlive:
		#Sends and receives messages over LoRa
		commProtocol.eventLoop()
		print("event loop running")
	

if __name__ == "__main__":
	main()
