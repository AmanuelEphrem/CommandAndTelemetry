import socket

s = socket.socket()
port = 12345
s.connect(('REPLACE WITH LOCAL IP OF PI', port))
st = "PogChamp"
byt = st.encode()
s.send(byt)
s.close()
