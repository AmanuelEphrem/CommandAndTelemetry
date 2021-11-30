import socket
import encoder

def main():
    img = encoder.encode_image("donut.png")
    s = socket.socket()
    port = 57762
    final = encoder.create_list(img)
    s.connect(('*SERVER IP*', port))
    s.send(len(final).to_bytes(100, 'big'))
    for i in range(len(final)):
        s.send(final[i])
    s.close()
if __name__ == "__main__":
    main()
