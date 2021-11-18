import encoder
from CommunicationProtocol import CommunicationProtocol

# def receiveMessage():
# 	packet = None
# 	# check for packet rx
# 	packet = loraRadio.receive(with_header = True)
# 	if packet == None:
# 		print("No Data Received")
# 		return None
# 	else:
# 		iden = packet[2]
# 		prev_packet = packet[4].decode("utf-8")
# 		if prev_packet == "IMAGE INCOMING":
# 			recImg(iden)
# 		return prev_packet

def recImg(imgLen: int):
    comm = CommunicationProtocol()
    comArr = [None] * imgLen
    i = 0
    dropPacket = 0
    while i < imgLen: # TODO: Update this implementation to deal with lost/dropped packets. 
        packet = comm.recPacket()
        if packet == None: # If we don't get a packet
            continue # Restart the loop
        i += 1
        num = packet[2] # Sets num equal to the identifier given to the packet. That should be it's location in the array.
        packet = packet[4:] # This SHOULD make packet equal to the actual passed bytearray with the header removed
#         j = 0 # If packet = packet[4:] doesn't work, uncomment this and the next 2 lines and comment out packet = packet[4:]
#         for j in range(4): # This removes the four header bytes from the bytearray. This can be done easier with a substring
#             packet.pop(0)
        comArr[num] = packet # Puts the packet(aka bytearray) in the location given by the identifier in the header.
    finArr = encoder.recombine_list(comArr)
    ans = encoder.decode_image(finArr, "newimg.png") # Placeholder name

def main():
    comm = CommunicationProtocol()
    while True:
        ans = comm._receiveJSON()
        if ans != None and ans['body'] == 'image':
            recImg(ans)

if __name__ == "__main__":
    main()