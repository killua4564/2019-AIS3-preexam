#!/usr/bin/env python3

# pylint: disable=import-error
from tensorflow.keras.models import load_model
import numpy as np

chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}'

def encode(string):
	'''Encode string into indeces according to chars.'''
	return np.array([chars.index(c) for c in string])

def decode(indeces):
	return ''.join(map(chars.__getitem__, indeces))

if __name__ == '__main__':
	model = load_model('model.h5')

	def top10(flag, score, max_score):
		if score > max_score[0][0]:
			max_score[0] = (score, flag)
			max_score.sort()

	def flag_score(x):
		return model.predict(x.reshape(1, -1))[0][0]

	# for i in itertools.product(chars[:-2], repeat=25):
	flag_list = [""]
	for r in range(25):
		max_score = [(0, "")] * 10
		for flag_ans in flag_list:
			for c in chars[:-2]:
				flag = encode("AIS3{{{iter}}}".format(iter=flag_ans + c + "X" * (24-r)))#"".join(i)))
				top10(flag_ans + c, flag_score(flag), max_score)
		flag_list = [flag_ans for _, flag_ans in max_score]
		print(flag_list)
	print("AIS3{{{flag}}}".format(flag=flag_list[-1]))
