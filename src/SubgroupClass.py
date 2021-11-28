#A class that represents a subgroup. Interfacing between subgroups should occur only in this class.
#todo: make necessary functions private. 
import Socket
import json
class SubgroupClass:
	
	#Constructor
	def __init__(self, subgroupValue:str, portValue:int):
		self.subgroup = subgroupValue
		self.payloadData = None
		self.subgropuData = None
		self.port = portValue
		self.socket = openSocket()
	
	#Setter for subgroupData
	def setSubgroupData(self,jsonData:dict):
		self.subgroupData = jsonData

	#Setter for payloadData
	def setPayloadData(self, jsonData:dict):
		self.payloadData = jsonData
	
	#Getter for payloadData
	def getPayloadData(self) -> dict:
		return self.payloadData

	#Getter for subgroupData
	def getSubgroupData(self) -> dict:
		return self.subgroupData

	#Sends payload to subgroup (using the specified port)
	def sendPayload(self) -> bool:
		#Attempts to open a new socket if socket doesn't exist	
		if self.socket == None:
			self.socket = openSocket()
			#returns false if socket still doesn't exist
			if self.socket == None:
				return False
		
		#sends payload through socket
		payloadString = json.dumps(self.payloadData)
		payloadString.encode("utf-8","strict")
		sendingPacket = bytes(payloadString,"utf-8")
		self.socket.sendall(sendingPacket)
		#resets payloadData after sending it
		self.payloadData = None
		return True


	#Attempts to open a socket on a specific port
	#@return  an open socket or None
	def openSocket(self) -> socket:
		openSocket = None
		socketHost = '127.0.0.1'
		socketPort = self.port
		try:
			openSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			openSocket.connect((socketHost,socketPort))
		except ConnectionRefusedError:
			openSocket = None	

		return openSocket
			

	#Returns a valid JSON string able to be sent over the communication protocol over the subgroupData
	#IMPORTANT: subgroupData must have a key "receiver"
	#IMPORTANT: resets subgroupData, so only call this function when use of subgroupData is no longer needed after function call
	def packageSubgroupData(self) -> str:
		if self.subgroupData == None:
			return None
		
		subgroupDataString = json.dumps(self.subgroupData)	
		validJSON = {"sender":self.subgroup,"receiver":self.subgroupData["receiver"],"type":"json","data":subgroupDataString}	
		#resets subgroupData after packaging it
		self.subgroupData = None
		return json.loads(validJSON)
