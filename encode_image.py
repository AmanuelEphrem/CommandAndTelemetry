import base64

#this file defines the functions encode_image and decode_image
#please be nice, if you are encoding a png decode it as a png, and so on with other file extentions

#this function takes an image and then returns that image as a string encoded with base64
#this function takes the Path to the image @imagename
def encode_image(imagename):
	binaryImage = open(imagename, 'rb')
	#print(binaryImage.read())
	image_string = base64.b64encode(binaryImage.read())
	#print(image_string)
	binaryImage.close()
	return image_string
	#return image_string

#this function converts an encoded string of an image and converts it back into an image
#this function needs the string to decode as @string2decode
#this function also needs how this image will be saved as @fileName 
def decode_image(string2decode, fileName):
	newImage = open(fileName, 'wb')
	newImage.write(base64.b64decode(string2decode))
	newImage.close()


#testing area
#encoded_image = encode_image("../routes.png")
#print("\n\n\n\n\n\n")
#print(encoded_image)
#print("88")
#decode_image(encoded_image, "rip.jpg")


