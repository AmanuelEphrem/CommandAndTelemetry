import json
import encoder
import CommunicationProtocol as comm

def sendImage(img_name):
	arr = encoder.encode_image(img_name)
	arr = encoder.create_list(arr)
	leng = len(arr)
	incoming_img = {"image" : leng}
	size_json = json.dumps(incoming_img)
	comm.communicateData(size_json)
	for i in range(leng):
		nextImg = {str(arr[i]) : i}
		next_json = json.dumps(nextImg)
		comm.communicateData(next_json)
# sendImage("donut.png")
