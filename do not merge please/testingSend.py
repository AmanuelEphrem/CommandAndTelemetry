import socket
import base64
import zlib
import math


def encodeImage(imgName):
	with open(imgName, "rb") as img_file:
		ans = bytearray(img_file.read())
	ans = zlib.compress(ans)
	ans = base64.b85encode(ans)
	return ans

def sendImage(imgName):
	encoded = encodeImage(imgName)
	size = math.ceil(len(encoded) / 250)
	print(size)
	n = 250
	chunks = [encoded[i:i+n] for i in range(0, len(encoded), n)]
	print(chunks)
	print(len(chunks))
	

def main():
	sendImage("donut.png")

main()