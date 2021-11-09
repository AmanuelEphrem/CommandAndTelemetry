import json
import encoder

def sendImage(img_name):
	arr = encoder.encode_image(img_name)
	arr = encoder.create_list(arr)
	leng = len(arr)
	incoming_img = {"INCOMING IMAGE" : leng}
	size_json = json.dumps(incoming_img)
	# Send json file line goes here
	for i in range(leng):
		nextImg = {str(arr[i]) : i}
		# Send json file line goes here
sendImage("donut.png")