import encoder
import json
from CommunicationProtocol import CommunicationProtocol
import time

def sendImg(imgname: str):
    comm = CommunicationProtocol()
    tempArr = encoder.encode_image(imgname)
    imgArr = encoder.create_list(tempArr)
    imgLen = len(imgArr)
    incImg = {"body" : "image", "size" : imgLen}
    inc_json = json.dumps(incImg)
    comm._sendJSON(inc_json)
    time.sleep(1)
    for i in range(imgLen):
        comm.sendPacket(imgArr[i], i, "bytearray")
        time.sleep(0.05)

def main():
    sendImg("donut.png")

if __name__ == "__main__":
    main()