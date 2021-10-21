import socket
import base64
import zlib

def decodeImage(yoshi):
	ans = base64.b85decode(yoshi)
	with open('newImg.png', "wb") as fh:
		fh.write(zlib.decompress(ans))

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
		poggers = c.recv(9000)
		print(poggers.decode())
		decodeImage(poggers)
		c.close()
		if poggers != None:
			startCounting = True
		if startCounting:
			i += 1
		if poggers != None and i > 0:
			print("\n" + str(i))
			exit()

main()
