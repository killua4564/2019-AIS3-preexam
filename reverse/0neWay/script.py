import idc

ea = 0x202010
ea_stop = 0x22ec59

with open("flag.jpg", "wb") as flag:
	while ea <= ea_stop:
		flag.write(chr(idc.Byte(ea)))
		ea += 1

#$ xortool flag.jpg -l 20 -c 20