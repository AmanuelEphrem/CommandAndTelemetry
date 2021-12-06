import socket
import threading
import json

class ThreadingClass:
	def thrSocket(groups: dict, addr):
		s = socket.socket()
		print("Socket")
		port = 12345
		s.bind((addr, port))
		print("Socket bound")
		s.listen(5)
		print("Listening")
		i = 0
		while True:
			c, addr = s.accept()
			print("Got connection from ", addr)
			recd = c.recv(10000)
			recd.decode("utf-8","strict")
			recd = json.loads(recd)
			groups[recd["sender"]].setSubGroupData(recd)

# def main(): # This shouldn't be called. It's pretty much all for testing.
# 	g = {1:2, 3:4}
# 	t1 = threading.Thread(target = thrSocket, daemon = True, args =(g,)) # IMPORTANT: Make sure the args value is a TUPLE. Since we're using one dict, it has to be formatted like (dict,)
# 	t1.start()
# 	i = 0
# 	while i < 100000:
# 		i += 1
# 	t1.join()
