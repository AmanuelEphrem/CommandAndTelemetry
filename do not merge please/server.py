import socket
import base64
import zlib
import numpy as np

def decodeImage(yoshi):
	ans = yoshi
	#ans = base64.b32decode(yoshi)
	with open('newImg.png', "wb") as fh:
		fh.write(zlib.decompress(ans))

def recombineImg(recimg):
	print("ops")

def main():
	s = socket.socket()
	print("Socket")
	port = 12345
	s.bind(('', port))
	print("Socket bounded")
	s.listen(5)
	print("listening")
	i = 0
	startCounting = False
	while True:
		c, addr = s.accept()
		print("Got connection from ", addr)
		poggers = c.recv(100)
		lenOfInp = int.from_bytes(poggers, byteorder='big')
		print(lenOfInp)
		tempArr = [None] * lenOfInp
		for i in range(lenOfInp):
			nextUp = c.recv(256)
			tempArr[i] = nextUp
		finArr = bytearray()
		for i in range(lenOfInp):
			finArr += tempArr[i]
		print(finArr)
		decodeImage(finArr)
		c.close()
		exit()
main()
