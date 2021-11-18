import encoder
import json
import busio 
from digitalio import DigitalInOut, Direction, Pull
import board # this is found only on raspberry pi
import adafruit_rfm9x 
from CommunicationProtocol import CommunicationProtocol

# THIS WILL BE REMOVED LATER - ITS IMPORTANT NOW FOR TESTING
#def loraSetup():
#	global loraRadio
#	CS = DigitalInOut(board.CE1)
#	RESET = DigitalInOut(board.D25)
#	spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
#	loraRadio = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
#	loraRadio.tx_power = 23

def sendImg(imgname: str):
    comm = CommunicationProtocol()
    tempArr = encoder.encode_image(imgname)
    imgArr = encoder.create_list(tempArr)
    imgLen = len(imgArr)
    incImg = {"body" : "image", "size" : imgLen}
    inc_json = json.dumps(incImg)
    comm.communicateData(inc_json)
    for i in range(imgLen):
        comm.sendPacket(imgArr[i], i, "bytearray")
#        sendMessage(imgArr[i], i)

def sendMessage(message, numSent):
    sendingPacket = message
    loraRadio.send(sendingPacket, identifier = numSent)

def main():
    loraSetup()
    sendImg("donut.png")

if __name__ == "__main__":
    main()