import json
import encoder
from CommunicationProtocol import CommunicationProtocol 

def sendImage(img_name):
#	arr = encoder.encode_image(img_name)
#	arr = encoder.create_list(arr)
#	leng = len(arr)
#	incoming_img = {"body" : "image", "size" : leng}
#	size_json = json.dumps(incoming_img)
#	comm.communicateData(size_json)
#	for i in range(leng):
#		nextImg = {str(arr[i]) : i}
#		next_json = json.dumps(nextImg)
#		comm.communicateData(next_json)
	comm = CommunicationProtocol()
	arr = encoder.encode_image(img_name)
	arr = encoder.create_list(arr)
	leng = len(arr)
	incoming_img = {"body" : "image", "size": leng}
	size_json = json.dumps(incoming_img)
	comm.communicateData(size_json)
	for i in range(leng):
		sendMessage(arr[i], i)

def sendMessage(message, numSent):
	sendingPacket = message
	loraRadio.send(sendingPacket, identifier = numSent)


def receiveImage(arrSize, newimg): # Enters this function if you received the "IMAGE" message
	imgarr = [None] * arrSize
	for i in range(arrSize):
		packet = loraRadio.recieve(with_header = True)
		imgarr[packet[2]] = packet[4]
	finarr = encoder.recombine_list(imgarr)
	encoder.decode_image(finarr, "newimg.png")

# sendImage("donut.png")