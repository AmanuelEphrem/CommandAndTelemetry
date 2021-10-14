import socket

s = socket.socket()
port = 12345
s.connect(('10.151.154.245', port))
st = "PogChamp"
byt = st.encode()
s.send(byt)
s.close()