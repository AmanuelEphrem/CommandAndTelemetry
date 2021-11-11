import json
import encoder
import CommunicationProtocol as comm

def sendImage(img_name):
	arr = encoder.encode_image(img_name)
	arr = encoder.create_list(arr)
	leng = len(arr)
	incoming_img = {leng : "image"}
	size_json = json.dumps(incoming_img)
	comm.communicateData(size_json)
	for i in range(leng):
		nextImg = {str(arr[i]) : i}
		next_json = json.dumps(nextImg)
		comm.communicateData(next_json)

def receiveImage(arrSize, newimg): # Enters this function if you received the "image" message
	imgarr = [None] * arrSize
	for i in range(arrSize):
		ans = comm.receiveData()
		tempkey = list(ans.keys())
		tempval = list(ans.values())
		imgarr[int(tempkey[0])] = bytearray(tempval[0])
	finarr = encoder.recombine_list(imgarr)
	encoder.decode_image(finarr, newimg)

# sendImage("donut.png")
