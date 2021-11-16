import socket

s = socket.socket()
port = 12345
s.connect(('lolcalhost', port))
st = "PogChamp"
byt = st.encode()
s.send(byt)
s.close()
