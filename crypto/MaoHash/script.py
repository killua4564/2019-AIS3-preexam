from math import cos

X = [int((0xFFFFFFFE) * cos(i)) & 0xFFFFFFFF for i in range(256)]

def G(X,Y,Z):
	return (X ^ (~Z | ~Y) ^ Z) & 0xFFFFFFFF
def H(X,Y,Z):
	return (X ^ Y ^ Z & X) & 0xFFFFFFFF
def I(X,Y,Z):
	return ((X & ~Z) | (~Z & Y)) & 0xFFFFFFFF
def J(X,Y,Z):
	return ((X ^ ~Z) | (X & ~Y)) & 0xFFFFFFFF
def K(X,Y,Z):
	return ((~X & Z) | (~X & Z ^ ~Y)) & 0xFFFFFFFF
def L(X,Y,Z):
	return ((~X & Y ^ Z) | (X & Y)) & 0xFFFFFFFF
def M(X,Y):
	return (X << Y | X >> (32 - Y)) & 0xFFFFFFFF

def mao192(s):
	A = 0x41495333
	B = 0x7b754669
	C = 0x6e645468
	D = 0x65456173
	E = 0x74657245
	F = 0x6767217D
	s_size = len(s)
	s += bytes([0xb0])
	if len(s) % 128 > 120:
		while len(s) % 128 != 0: s += bytes(1)
	while len(s) % 128 < 120: s += bytes(1)
	s += bytes.fromhex(hex(s_size * 8)[2:].rjust(16, '0'))
	for index, byte in enumerate(s):
		k, l = int(byte), index & 0x1f
		A = (B + M(A + G(B,C,D) + X[k], l)) & 0xFFFFFFFF
		B = (C + M(B + H(C,D,E) + X[k], l)) & 0xFFFFFFFF
		C = (D + M(C + I(D,E,F) + X[k], l)) & 0xFFFFFFFF
		D = (E + M(D + J(E,F,A) + X[k], l)) & 0xFFFFFFFF
		E = (F + M(E + K(F,A,B) + X[k], l)) & 0xFFFFFFFF
		F = (A + M(F + L(A,B,C) + X[k], l)) & 0xFFFFFFFF
	return ''.join(map(lambda x : hex(x)[2:].rjust(8, '0'), [A, F, C, B, D, E]))

def hack_mao192(mac, s, start=128): # s = append_string
	A, F, C, B, D, E = [int(mac[i:i+8], 16) for i in range(0, len(mac), 8)]
	s_size = len(s)
	s += bytes([0xb0])
	if len(s) % 128 > 120:
		while len(s) % 128 != 0: s += bytes(1)
	while len(s) % 128 < 120: s += bytes(1)
	s += bytes.fromhex(hex((s_size + start) * 8)[2:].rjust(16, '0'))
	for index, byte in enumerate(s):
		k, l = int(byte), index & 0x1f
		A = (B + M(A + G(B,C,D) + X[k], l)) & 0xFFFFFFFF
		B = (C + M(B + H(C,D,E) + X[k], l)) & 0xFFFFFFFF
		C = (D + M(C + I(D,E,F) + X[k], l)) & 0xFFFFFFFF
		D = (E + M(D + J(E,F,A) + X[k], l)) & 0xFFFFFFFF
		E = (F + M(E + K(F,A,B) + X[k], l)) & 0xFFFFFFFF
		F = (A + M(F + L(A,B,C) + X[k], l)) & 0xFFFFFFFF
	return (''.join(map(lambda x : hex(x)[2:].rjust(8, '0'), [A, F, C, B, D, E]))).encode()

def hash(*stuff):
	return mao192(b'&&'.join(stuff)).encode()

def proof():
	username = b"Admin"
	password = b"sec"
	session = b"48bb668c85ea50cfc1f7" # len = 20
	mac = hash(username, password, session)

	length = 32
	session_fake = session + b"\xb0" + b"\x00" * (120-length-1) + bytes.fromhex(hex(length * 8)[2:].rjust(16, '0'))
	cmd = b"flag"

	print(hash(username, password, session_fake, session, cmd))
	print(hack_mao192(mac, b"&&" + session + b"&&" + cmd))

from pwn import *
if __name__ == '__main__':
	for length in range(29, 100):
		conn = remote("maojui.me", "11111")
		conn.recvuntil(" : ")
		conn.sendline("Admin")
		conn.recvuntil(": ")
		session = conn.recvuntil("\n").strip(b"\n")
		conn.recvuntil(" : ")
		mac = conn.recvuntil("\n").strip(b"\n")
		conn.recvuntil("?\n")

		cmd = b"flag"
		session_fake = session + b"\xb0" + b"\x00" * (120-length-1) + bytes.fromhex(hex(length * 8)[2:].rjust(16, '0'))
		mac = hack_mao192(mac, b"&&" + session + b"&&" + cmd)
		conn.sendline(b"&&".join([mac, session_fake, session, cmd]))
		print(length, conn.recv())
		conn.close()
		
	# len=93, AIS3{imP13M3NT_Lea_I5_N0T_Soooo_HARD_right_xdddd}


