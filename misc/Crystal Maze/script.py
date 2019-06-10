from pwn import *

E = ["up", "down", "left", "right"]

def action(conn, move):
	conn.recvuntil("move: ")
	conn.sendline(move)
	value = conn.recvuntil("\n")
	if b"AIS3" in value:
		print(value)
		exit()
	return b"ok" in value

def maze(step=[""]):
	print(step)
	for e in E:
		if step[-1] == "up" and e == "down": continue
		if step[-1] == "down" and e == "up": continue
		if step[-1] == "left" and e == "right": continue
		if step[-1] == "right" and e == "left": continue

		conn = remote("pre-exam-chals.ais3.org", "10202")

		conn.recvuntil(".\n")
		conn.recvuntil(".\n")

		for s in step[1:]: action(conn, s)

		if action(conn, e): maze(step + [e])
		
		conn.close()

maze()