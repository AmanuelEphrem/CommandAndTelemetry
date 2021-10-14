import busio
import digitalio
import board
import adafruit_rfm9x

RADIO_FREQ_MHZ = 915.0
CS = digitialio.DigitalInOut(board.CE1) # CHANGE BASED ON HOW IT IS WIRED
RESET = digitalio.DigitalInOut(board.D25) # CHANGE BASED ON HOW IT IS WIRED
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

rfm9x.signal_bandwith = 62500
rfm9x.coding_rate = 6
rfm9x.spreading_factor = 8
rfm9x.enable_crc = True

# Sending

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                         #
# Pretend this somehow gets the data we need and stores it intelligently  #
#                                                                         #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

data = bytes(sensor_data.json) # I don't know how we send stuff as a .json with LoRa. This might need to be in strings.
rfmj9x.send(data)