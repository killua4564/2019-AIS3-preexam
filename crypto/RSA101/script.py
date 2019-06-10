from pwn import *
from sympy import invert
from Crypto.Util.number import long_to_bytes

conn = remote("pre-exam-chals.ais3.org", "10201")

f = lambda x: int(str(x, "utf-8"))
conn.recvuntil(" : (")
e, n = map(f, conn.recvuntil(")\n").strip(b")\n").split(b","))

conn.recvuntil(" : ")
c = f(conn.recvuntil("\n").strip(b"\n"))

conn.recvuntil(" : \n")

delta = 2
left, right = 1, n
while delta > 1:
	center = (left + right) // 2
	conn.recvuntil("n = ? \n")
	conn.sendline(str(center))
	conn.recvuntil(" = ")
	remainder = f(conn.recvuntil("\n").strip(b"\n"))
	if remainder == center % 64:
		left = center
	else: right = center
	delta = right - left
	print("delta:", delta)

phi = right
d = int(invert(e, phi))
m = pow(c, d, n)
print(long_to_bytes(m))

# AIS3{RSA_L0L_01100110011101010110001101101011}