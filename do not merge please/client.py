import socket
import base64
import zlib
import math
import numpy as np
import time

def encode_image():
    with open ("donut.png", "rb") as img_file:
        ans = bytearray(img_file.read())
    print(ans)
    ans = zlib.compress(ans)
    print(len(ans))
    return ans

def createList(img_whole):
    size = math.ceil(len(img_whole)/250)
    print(size)
    fin_arr = [img_whole[i:i+250] for i in range(0, len(img_whole), 250)]
    print(len(fin_arr))
    return fin_arr

def main():
    img = encode_image()
    s = socket.socket()
    port = 12345
    final = createList(img)
    s.connect(('10.151.132.101', port))
    s.send(len(final).to_bytes(100, 'big'))
    time.sleep(1)
    for i in range(len(final)):
        s.send(final[i])
    s.close()

main()