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
    while i < imgLen: # TODO: Update this implementation to deal with lost/dropped packets. 
        packet = comm.recPacket(500)
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

def recImgTest(imgLen: int):
    comm = CommunicationProtocol()
    comArr = [None] * imgLen # Makes an empty array of the size of the length of the image. Sample(if imgLen = 12): [None, None, None, None, None, None, None, None, None, None, None, None]
    assembled = 0 # Keeps a counter of the total number of packets successfully received and put in their correct spot
    i = 0 # Keeps a counter of the number of packets received from the last 5
    recPackets = [] # Contains received packets out of the last 5 (hopefully) sent. Sample: [b(1234), b(5678), b(7890)]
    recNums = [] # Contains the location in the comArr of the received packets. Sample: [6, 7, 10]
    locPos = [] # Contains which packet out of 5 expected the received packet/num combo at the same location. Sample: [0, 1, 4]
    while assembled < imgLen: # If we have the same number (or greater) of assembled packets as we expected, end this loop.
        if i >= 5: # This is the same at at the bottom of the loop, but this just catches it if the last packet was None
            failed = checkLoc(locPos)
            comm.sendPacket(failed, 0, "int")
            i = 0
            recPackets = []
            recNums = []
            locPos = []
            continue
        packet = comm.recPacket(500) # Wait 500 for a packet
        if packet == None: # If no packet was received
            i += 1 # Increment i and restart the loop
            continue
        i += 1 # Otherwise, increment i
        num = packet[2] # Set num equal to the identifier
        packet = packet[4:] # Set the packet equal to the sent packet
        comArr[num] = packet # Put the packet in the location specified by the identifier
        recPackets.append(packet) # Put the received packet at the end of the recPackets list
        recNums.append(num) # Put it's corresponding number in the same location in the recNums
        locPos.append(i) # Put it's corresponding i in the same location in locPos
        assembled += 1 # Add 1 to assembled, since a packet was successfully received.
        if i >= 5: # If we received 5 packets since the last time we checked
            failed = checkLoc(locPos) # Gets the number sent back to sendImg of packets that were not received.
            comm.sendPacket(failed, 0, "int") # Sends that number
            i = 0 # Resets i
            recPackets = [] # Resets recPackets
            recNums = [] # Resets recNums
            locPos = [] # Resets locPos
    finArr = encoder.recombine_list(comArr)
    ans = encoder.decode_image(finArr, "newimg.png")

def checkLoc(locPos) -> int:
            num = 0 # Set num to 0
            for j in reversed(locPos): # Go through a reversed version of locPos
                num >> j
                num |= 1
                num << j
            num ^= 31
            return num

def main():
    comm = CommunicationProtocol()
    while True:
        ans = comm._receiveJSON()
        if ans != None and ans['body'] == 'image':
            recImgTest(ans)

if __name__ == "__main__":
    main()