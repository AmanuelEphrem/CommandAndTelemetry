import socket
import base64
import zlib

def encode_image():
    with open ("pixel.png", "rb") as img_file:
        ans = bytearray(img_file.read())
    ans = zlib.compress(ans)
    ans = base64.b85encode(ans)
    print(ans.decode())
    return ans

def main():
    len = encode_image()
    s = socket.socket()
    port = 12345
    s.connect(('192.168.1.171', port))
    s.send(len)
    s.close()

main()