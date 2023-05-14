import hashlib

# Edit just these variables
filepath1 = ""
filepath2 = ""

text1 = None
text2 = None

with open(filepath1, "r") as file1:
	text1 = file1.read()

with open(filepath2, "r") as file2:
	text2 = file2.read()

if not text1 or not text2:
	print("Couldn't open both files.  Text1={}, Text2={}".format(text1, text2))
	exit(0)

if len(text1) != len(text2):
	print("Text lengths are different")
	exit(0)

bytes1 = []
bytes2 = []

index = 0
len_text1 = len(text1)
len_text2 = len(text2)
while(True):

	if index >= len_text1 and index >= len_text2:
		break
	if index < len_text1:
		bytes1.append(ord(text1[index]))
	if index < len_text2:
		bytes2.append(ord(text2[index]))
	index += 1

hash1 = hashlib.sha1()
hash2 = hashlib.sha1()


byteobj1 = bytes(bytes1)
byteobj2 = bytes(bytes2)

hash1.update(byteobj1)
hash2.update(byteobj2)

hash1_bytes = hash1.digest()
hash2_bytes = hash2.digest()

print("Hash 1:\n{}".format(hash1_bytes))
print("Hash 2:\n{}".format(hash2_bytes))
if hash1_bytes == hash2_bytes:
	print("Texts are the same")
else:
	print("Texts are different")
