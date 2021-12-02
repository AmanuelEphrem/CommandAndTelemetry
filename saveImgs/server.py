import socket
import threading
import encoder

def main():
	s = socket.socket()
	print("Socket")
	port = 57762
	s.bind(('*LOCAL IP*', port))
	print("Socket bound")
	s.listen(5)
	print("Listening")
	while True:
		c, addr = s.accept()
		print(addr)
		print("Got connection from ", addr)
		recd = c.recv(100)
		lenOfInp = int.from_bytes(recd, byteorder='big')
		print(lenOfInp)
		tempArr = [None] * lenOfInp
		for i in range(lenOfInp):
			nextUp = c.recv(256)
			tempArr[i] = nextUp
		finArr = encoder.recombine_list(tempArr)
		encoder.decode_image(finArr, "imgName%d.png"%addr[1])
if __name__ == "__main__":
    main()