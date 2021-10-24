#Sending data from Lora chip
# Need 2nd lora Chip this prolly does not work tho
#-juan
import time
import board
import busio
import adafruit_rfm9x
from digitalio import DigitalInOut
from adafruit_tinylora.adafruit_tinylora import TTN,TinyLoRa

spi = busio.SPI(board.SCK,MOSI=board.MOSI,MISO=board.MISO)
cs = DigitalInOut(board.CE1)
irq = DigitalInOut(board.D5)
rst = DigitalInOut(board.D25)

# TTN device addy, network and app key
devaddr = bytearray([0x00,0x00,0x00,0x00])
nwkey = bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
app = bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

ttn_config = TTN(devaddr,nwkey,app,country='US')
lora = TinyLoRa(spi,cs,irq,rst,ttn_config,channel = 6)

data = bytearray([0x01,0x02])
while True:
    print("Sending Hi...")
    lora.send_data(data,len(data),lora.frame_counter)
    print("Packet sent!")
    lora.frame_counter +=1
    time.sleep(30)
