import socket

def main():
	s = socket.socket()
	print("Socket")
	port = 12345
	s.bind(('', port))
	print("Socket bounded")
	s.listen(5)
	print("listening")
	while True:
		c, addr = s.accept()
		print("Got connection from ", addr)
		poggers = c.recv(1024)
		print(poggers.decode())
		c.close()

main()