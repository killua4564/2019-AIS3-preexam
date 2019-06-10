# a = open("challenge_0.png", "rb").read()
# b = open("challenge_1.png", "rb").read()

# with open("test.png", "wb") as file:
# 	for i, j in zip(a, b):
# 		file.write(chr(i ^ j))

import cv2
from Crypto.Util.number import long_to_bytes

images = [cv2.imread('challenge_{}.png'.format(str(i))) for i in range(51)]

# for i in range(50):
# 	for j in range(i+1, 51):
# 		xor = cv2.bitwise_xor(images[i], images[j])
# 		cv2.imwrite('result_xor/{}xor{}.png'.format(str(i), str(j)), xor)

# for i in range(50):
# 	for j in range(i+1, 51):
# 		xor = cv2.bitwise_and(images[i], images[j])
# 		cv2.imwrite('result_and/{}and{}.png'.format(str(i), str(j)), xor)

# for i in range(50):
# 	for j in range(i+1, 51):
# 		xor = cv2.bitwise_or(images[i], images[j])
# 		cv2.imwrite('result_or/{}or{}.png'.format(str(i), str(j)), xor

image = images[0]
for i in range(1, 51):
	image = cv2.bitwise_xor(image, images[i])
	cv2.imwrite("xor.png", image)

image = images[0]
for i in range(1, 51):
	image = cv2.bitwise_or(image, images[i])
	cv2.imwrite("or.png", image)

image = images[0]
for i in range(1, 51):
	image = cv2.bitwise_and(image, images[i])
	cv2.imwrite("and.png", image)

# for i in range(51):
# 	image = cv2.imread('challenge_{}.png'.format(str(i)))
# 	for row in image:
# 		text = long_to_bytes(int("".join(["0" if cloumn[0] == 255 else "1" for cloumn in row]), 2))
# 		if b"AIS3" in text:
# 			print(text)


