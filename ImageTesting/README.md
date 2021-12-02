**Identifier change explanation:**
num = Location in final array = 7 = b(111)
j = Location in sending array = 3 = b(011)
num <<= 3 -> b(111000)
num |= j -> (b111011)
Sends num across
ans = position in received array = 7 = b(111)
ans &= num -> b(000011) = 3
num >>= 3 b(111)
Preserves original num while also bringing over the original location.
Since we only send 5 packets at a time, this is OK to be hardcoded in like this.

PSEUDOCODE EXPLANATION:
sendImgTest:
  incImg encoded into json and sent to receiving location
  Creates two empty lists named packToSend and numToSend for holding packets and nums to send.
  Creates two variables equal to zero named numSent and i
  i will point to the location in the array we need to be and numSent is the number of successful packets sent.
  LOOP: While all packets have not been sent
  Create/empty arrays prevPacks and prevNums
  While there are less than 5 packets waiting to be sent AND i is less than the length of the array (aka i is pointing to a value inside the array)
    Add the packet i is pointing to to the packets to send list
    Add the position that packet is supposed to go in (i) to the nums to send list
    Increment i
  Create a variable that is equal to the length of the packets to send waiting list
  Then, iterate through that list
    Pop the top value off the waiting list
    Pop the top num off the waiting list
    Send them both across
    Put the packet into the prevPacket list
    Put the num into the prevNums list
    Add 1 to numSent
  Once you're done iterating through the list, then wait and listen for a response from the recImgTest file
  Once it's received, turn it into an int
  Create a variable named dropped, which is equal to 0
  Then, while that int is > 0
    See if it's & with 1 is 1.
      If it is, put the prevPacket and prevNum at the location "dropped" in their arrays back into the packToSend list
      Remove 1 from numSent (since it was not successfully sent)
    Then rightshift the given int by 1 and increment dropped by 1
  
  recImgTest:
    Create an array to receive all the received values
    Create a counter to track how many packets you've received
    Create a counter to track how many packets you've received out of 5
    Create empty arrays to store the received packets, the received numbers, and the i values for those.
    While you have less received packets than the number of expected received packets
      If i >= 5, create a number of dropped packets and send that to sendImgTest.
        Reset all the temporary counters (i, recPackets, recNums, locPos)
        Then restart the loop.
        This exists here so if you drop the last packet you don't try to get more than 5 packets
      Otherwise, wait for a packet
      If you don't get a packet, increment i and restart the loop
      If you do get a packet, increment i and then get the index that packet is supposed to go and the packet itself
      Then put the packet in it's corresponding location.
      Then save that packet in recPackets, it's index in recNums, and it's associated i value in locPos
      Add 1 to the number of received packets
      Then, check if you have received 5 or more packets since the last time you checked.
        If you have, get the number of failed packets you received and send it to sendImgTest
        Reset all the temporary counters (i, recPackets, recNums, locPos)
        And restart the loop
    Create an array that combines all of the packets you received
    Then take that array and decode it and put it in a file.
  
***EXAMPLE EXPECTED RUN OF THE CODE***:
b() indicates a bytearray.
Example array: b(abcdefghijklmnopqrst)
imgArr = [b(abcd), b(efgh), b(ijkl), b(mnop), b(qrst)]
imgLen = 5
incImg = {"body": "image", "size": 5}
  Sample run (with above given info)
   sendImgTest:
    numSent = 0, imgLen = 5, i = 0, packToSend = [], numToSend = []
    numSent < imgLen so continue
    prevPacks emptied, prevNums emptied
    len(packToSend) is 0, so < 5 and 0 < 5, so start appending
      packToSend[b(abcd)]
      numToSend[0]
      i++
      i = 1
      
    len(packToSend) is 1, so < 5, and 1 < 5
      packToSend[b(abcd), b(efgh)]
      numToSend[0, 1]
      i++
      i = 2
      
    len(packToSend) is 2, so < 5, and 2 < 5
      packToSend[b(abcd), b(efgh), b(ijkl)]
      numToSend[0, 1, 2]
      i++
      i = 3
      
    3 < 5 and 3 < 5
      packToSend[b(abcd), b(efgh), b(ijkl), b(mnop)]
      numToSend[0, 1, 2, 3]
      i++
      i = 4
      
    4 < 5 and 4 < 5
      packToSend[b(abcd), b(efgh), b(ijkl), b(mnop), b(qrst)]
      numToSend[0, 1, 2, 3, 4]
      i++
      i = 5
      
    5 is NOT < 5, so stop looping
    cycle = len(packToSend) so cycle = 5
    For j = 0
      tempPack = b(abcd)
      tempNum = 0
      send tempPack, tempNum
      prevPack = [b(abcd)]
      prevNum = [0]
      packToSend = [b(efgh), b(ijkl), b(mnop), b(qrst)]
      numToSend = [1, 2, 3, 4]
      numSent = 1
      
    For j = 1
      tempPack = b(efgh)
      tempNum = 1
      send tempPack, tempNum
      prevPack = [b(abcd), b(efgh)]
      prevNum = [0, 1]
      packToSend = [b(ijkl), b(mnop), b(qrst)]
      numToSend = [2, 3, 4]
      numSent = 2
      
    For j = 2
      tempPack = b(ijkl)
      tempNum = 2
      send tempPack, tempNum
      prevPack = [b(abcd), b(efgh)], b(ijkl)]
      prevNum = [0, 1, 2]
      packToSend = [b(mnop), b(qrst)]
      numToSend = [3, 4]
      numSent = 3
      
    For j = 3
      tempPack = b(mnop)
      tempNum = 3
      send tempPack, tempNum
      prevPack = [b(abcd), b(efgh)], b(ijkl), b(mnop)]
      prevNum = [0, 1, 2, 3]
      packToSend = [b(qrst)]
      numToSend = [4]
      numSent = 4
      
    For j = 4
      tempPack = b(qrst)
      tempNum = 4
      send tempPack, tempNum
      prevPack = [b(abcd), b(efgh)], b(ijkl), b(mnop), b(qrst)]
      prevNum = [0, 1, 2, 3, 4]
      packToSend = []
      numToSend = []
      numSent = 5
      
    Done looping
    Listen for response for dropped packets from recImgTest
    prevPack = [b(abcd), b(efgh)], b(ijkl), b(mnop), b(qrst)]
    prevNum = [0, 1, 2, 3, 4]
    packToSend = []
    numToSend = []
    numSent = 5
    
    Received response from recImgTest
    hold = 12 (01100)
    dropped = 0
    prevPack = [b(abcd), b(efgh)], b(ijkl), b(mnop), b(qrst)]
    prevNum = [0, 1, 2, 3, 4]
    packToSend = []
    numToSend = []
    numSent = 5
    
    Hold > 0 so
      01100 & 1 = 0 so nothing happens
      Rightshift hold by 1 (0110)
      Add 1 to dropped
      hold = 6 (0110)
      dropped = 1
      prevPack = [b(abcd), b(efgh)], b(ijkl), b(mnop), b(qrst)]
      prevNum = [0, 1, 2, 3, 4]
      packToSend = []
      numToSend = []
      numSent = 5
    
    Hold > 0 so
      0110 & 1 = 0 so nothing happens
      Rightshift hold by 1 (011)
      Add 1 to dropped
      hold = 3 (011)
      dropped = 2
      prevPack = [b(abcd), b(efgh)], b(ijkl), b(mnop), b(qrst)]
      prevNum = [0, 1, 2, 3, 4]
      packToSend = []
      numToSend = []
      numSent = 5
    
    Hold > 0 so
      011 & 1 = 1 so something happens
        Add prevPack[dropped] to packToSend
        Add prevNum[dropped] to numToSend
        Remove 1 from numSent
      Rightshift hold by 1
      Add 1 to dropped
      hold = 1 (01)
      dropped = 3
      prevPack = [b(abcd), b(efgh)], b(ijkl), b(mnop), b(qrst)]
      prevNum = [0, 1, 2, 3, 4]
      packToSend = [b(ijkl)]
      numToSend = [2]
      numSent = 4

    Hold > 0 so
    01 & 1 = 1 so something happens
        Add prevPack[dropped] to packToSend
        Add prevNum[dropped] to numToSend
        Remove 1 from numSent
      Rightshift hold by 1
      Add 1 to dropped
      hold = 0 (0)
      dropped = 4
      prevPack = [b(abcd), b(efgh)], b(ijkl), b(mnop), b(qrst)]
      prevNum = [0, 1, 2, 3, 4]
      packToSend = [b(ijkl), b(mnop)]
      numToSend = [2, 3]
      numSent = 3
      
    Hold is no longer > 0, so restart the loop
    prevPack = [b(abcd), b(efgh)], b(ijkl), b(mnop), b(qrst)]
    prevNum = [0, 1, 2, 3, 4]
    packToSend = [b(ijkl), b(mnop)]
    numToSend = [2, 3]
    numSent = 3
    
    numSent is less than imgLen (3 < 5)
    Reset prevPacks and prevNums
    prevPack = []
    prevNum = []
    packToSend = [b(ijkl), b(mnop)]
    numToSend = [2, 3]
    numSent = 3
    len(packToSend) < 5 BUT i is not < imgLen (5 < 5) so skip adding more values to packToSend
    cycle = len(packToSend) so cycle = 2
    Go twice
    For j = 0
      tempPack = b(ijkl)
      tempNum = 2
      send tempPack, tempNum
      prevPack = [b(ijkl)]
      prevNum = [2]
      packToSend = [b(mnop)]
      numToSend = [3]
      numSent = 4
      
    For j = 1
      tempPack = b(mnop)
      tempNum = 3
      send tempPack, tempNum
      prevPack = [b(ijkl), b(mnop)]
      prevNum = [2, 3]
      packToSend = []
      numToSend = []
      numSent = 5
    Wait for response from recImgTest.py
    Received response - hold = 0
    Hold is not greater than 0, so stop running.
    
    
  recImgTest:
 Checks to make sure assembled is less than imgLen (0 < 5)
 Checks if i < 5. It is, so nothing special happens.
 For i = 0: receives a packet. Gets the location of that packet in the array (0) and the packet (b(abcd))
 Puts that packet in the correct spot in the comArr. Also saves it to recPackets, its num to recNums, and its i to locPos]
 Adds 1 to assembled
 comArr = [b(abcd), None, None, None, None]
 recPackets = [b(abcd)]
 recNums = [0]
 locPos = [0]
 assembled = 1
 Increments i and checks if i < 5. It is, so it restarts the loop.

 Checks to make sure assembled is less than imgLen (1 < 5)
 Checks if i < 5. It is, so nothing special happens.
 For i = 1: receives a packet. Gets the location of that packet in the array (1) and the packet (b(efgh))
 Puts that packet in the correct spot in the comArr. Also saves it to recPackets, its num to recNums, and its i to locPos
 Adds 1 to assembled.
 comArr = [b(abcd), b(efgh), None, None, None]
 recPackets = [b(abcd), b(efgh)]
 recNums = [0, 1]
 locPos = [0, 1]
 assembled = 2
 Increments i and checks if i < 5. It is, so it restarts the loop.

 Checks to make sure assembled is less than imgLen (2 < 5)
 Checks if i < 5. It is, so nothing special happens.
 For i = 2: No packet was received. Increment i and then restart the loop.
 comArr = [b(abcd), b(efgh), None, None, None]
 recPackets = [b(abcd), b(efgh)]
 recNums = [0, 1]
 locPos = [0, 1]
 assembled = 2
 
 Checks to make sure assembled is less than imgLen (2 < 5)
 Checks if i < 5. It is, so nothing special happens.
 For i = 3: No packet was received. Increment i and then restart the loop.
 comArr = [b(abcd), b(efgh), None, None, None]
 recPackets = [b(abcd), b(efgh)]
 recNums = [0, 1]
 locPos = [0, 1]
 assembled = 2

 Checks to make sure assembled is less than imgLen (2 < 5)
 For i = 4: receives a packet. Gets the location of that packet in the array (4) and the packet (b(qrst))
 Puts that packet in the correct spot in the comArr. Also saves it to recPackets, its num to recNums, and its i to locPos
 comArr = [b(abcd), b(efgh), None, None, b(qrst)]
 recPackets = [b(abcd), b(efgh), b(qrst)]
 recNums = [0, 1, 4]
 locPos = [0, 1, 4]
 assembled = 3
 Increments i and checks if i < 5. It isn't, so it starts this last part.
 
 Passes the locPos array to checkLoc
     checkLoc creates an int with value 0.
     Then it reverses the locPos array and iterates through each value in the list.
     num rightshifts over j, then OR's itself with 1 then leftshifts over j.
     Then num XOR's itself with 31 (11111) and returns.
     SAMPLE:
     j = 4
     num >> 4 -> 0
     num |= 1 -> 1
     num << 4 -> 10000
     j = 1
     num >> 1 -> 1000
     num |= 1 -> 1001
     num << 1 -> 10010
     j = 0
     num >> 0 -> 10010
     num |= 1 -> 10011
     num << 0 -> 10011
     num ^= 31 -> 10011 ^ 11111 = 01100
     Returns num
 Sends num back to sendImg.py. 1 = Failed to receive 0 = Successfully received.
 Resets i, locPos, recNums, and recPackets.
 Restarts loop
 comArr = [b(abcd), b(efgh), None, None, None]
 recPackets = []
 recNums = []
 locPos = []
 i = 0
 assembled = 3
 
 Checks to make sure assembled is less than imgLen (3 < 5)
 Checks if i < 5. It is, so nothing special happens.
 For i = 0: receives a packet. Gets the location of that packet in the array (2) and the packet (b(ijkl))
 Puts that packet in the correct spot in the comArr. Also saves it to recPackets, its num to recNums, and its i to locPos
 comArr = [b(abcd), b(efgh), b(ijkl), None, b(qrst)]
 recPackets = [b(ijkl)]
 recNums = [2]
 locPos = [0]
 Increments i and checks if i < 5. It is, so it restarts the loop.
 
 Checks to make sure assembled is less than imgLen (4 < 5)
 Checks if i < 5. It is, so nothing special happens.
 For i = 0: receives a packet. Gets the location of that packet in the array (3) and the packet (b(mnop))
 Puts that packet in the correct spot in the comArr. Also saves it to recPackets, its num to recNums, and its i to locPos
 comArr = [b(abcd), b(efgh), b(ijkl), b(mnop), b(qrst)]
 recPackets = [b(ijkl), b(mnop)]
 recNums = [2, 3]
 locPos = [0, 1]
 Increments i and checks if i < 5. It is, so it restarts the loop.
 
 Checks if assembled is less than imgLen (5 < 5)
 Assembled is not less than imgLen, so it stops.
 
 Combines comArr into one big array
 comArr = [b(abcd), b(efgh), b(ijkl), b(mnop), b(qrst)]
 finArr = b(abcdefghijklmnopqrst)
 Then it decodes that bytearray and writes it to a file.