import sys
sys.path.append("..") # Adds higher directory to python modules path.
import CommunicationProtocol
import SubgroupClass
import ThreadingClass
import Threading
def main():
	#Defines the port and instantiates subgroup objects
	sensoryPort = 12345
	faultManagementPort = 749742
	machineLearningPort = 83298
	sensoryGroup= SubgroupClass("sensory",sensoryPort)
	faultManagementGroup = SubgroupClass("faultManagement",faultManagementPort)
	machineLearningGroup = SubgroupClass("machineLearning",machineLearningPort)

	dictOfSubgroup = {"sensory":sensoryGroup,"faultManagement":faultManagementGroup,"machineLearning":machineLearningGroup}
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
