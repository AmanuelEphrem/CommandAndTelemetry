import socket
import base64
import zlib

def encode_image():
    with open ("donut.png", "rb") as img_file:
        ans = bytearray(img_file.read())
    print(ans)
    ans = zlib.compress(ans)
    #ans = base64.b32encode(ans)
    print(len(ans))
    return ans

def main():
    len = encode_image()
    s = socket.socket()
    port = 12345
    s.connect(('10.151.156.213', port))
    s.send(len)
    s.close()

main()