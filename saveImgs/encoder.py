import zlib
import math

# This function takes in a string that is the name ***INCLUDING FILE EXTENSION*** of the image to be encoded.
# Returns a compressed bytearray of the encoded image
def encode_image(imgname):
	with open(imgname, "rb") as img_file:
		ans = bytearray(img_file.read())
	ans = zlib.compress(ans)
	return ans

# encimg expects a bytearray of the img that wants to be decoded
# newimg expects a filename ***INCLUDING FILE EXTENSION, WHICH MATCHES ORIGINAL FILE TYPE OF ENCIMG*** to write into
def decode_image(encimg, newimg):
	try:
		with open(newimg, "wb") as fh:
			fh.write(zlib.decompress(encimg))
		return True
	except:
		return False

# img_whole expects the bytearray representation of an image to be split into subarrays
# returns an array of bytearrays which make up the input
def create_list(img_whole):
	#num = math.ceil(len(img_whole)/250)
    fin_arr = [img_whole[i:i+240] for i in range(0, len(img_whole), 240)] # Splits the bytearray into n bytearrays, where n is the value of the length of img_whole / 200 rounded up.
    return fin_arr # Returns the array containing all n bytearrays generated in the previous instruction.

# img_sep expects an array of bytearrays
# returns a bytearray that is a combined version of the passed in arrays.
def recombine_list(img_sep):
	ans = bytearray()
	for i in range(len(img_sep)):
		ans += img_sep[i]
	return ans
