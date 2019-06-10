#!/usr/bin/python
import os
import sys

black_list = "bcfghijkmnoqstuvwxz!@#|[]{}\"'&*()?01234569"

white_list = "adelpry78$^-_+="

your_input = raw_input(":")

for i in range(len(black_list)):
    if black_list[i] in your_input:
        print "Bad hacker...."
        exit()

print os.system("bash -c '" + your_input + "'")

# $SHELL
