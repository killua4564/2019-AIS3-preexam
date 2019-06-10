from pwn import *
from sympy import invert, gcd

conn = remote("pre-exam-chals.ais3.org", 10200)

conn.recvuntil(":\n")
conn.recvuntil(" \n")

n = list(map(int, str(conn.recvuntil("\n").strip(b"\n").strip(b"N = "), 'utf-8').split(', ')))

conn.recvuntil("+\n")
'''
N1 = a * N0 + b % c
N2 = a * N1 + b % c
N3 = a * N2 + b % c
N4 = a * N3 + b % c

N2 - N1 = a * (N1 - N0) % c ... (1)
N3 - N2 = a * (N2 - N1) % c ... (2)
N4 - N3 = a * (N3 - N2) % c ... (3)

first:
N0 * N3 = N0 * (a * N2 + b) % c
N1 * N2 = (a * N0 + b) * N2 % c

so:
N0 * N3 - N1 * N2 % c = 0

(1) * (3) - (2) * (2) % c
==> a ** 2 * (N1 - N0) * (N3 - N2) - a ** 2 * (N2 - N1) * (N2 - N1) % c = 0
==> (N2 - N1) * (N4 - N3) - (N3 - N2) * (N3 - N2) % c = 0

'''
c = abs((n[1] - n[0]) * (n[3] - n[2]) - (n[2] - n[1]) * (n[2] - n[1]))
for i in range(4, 10):
	c = gcd(abs((n[i-2] - n[i-3]) * (n[i] - n[i-1]) - (n[i-1] - n[i-2]) * (n[i-1] - n[i-2])), c)

for index in range(1, 10):
	c = c // gcd(n[index-1] - n[index], c)

a = int(invert(n[1] - n[0], c)) * (n[2] - n[1]) % c
b = (n[1] - a * n[0]) % c
f = lambda x: (a * x + b) % c

x = n[-1]
for _ in range(100):
	x = f(x)
	conn.sendline(str(x))
	conn.recvuntil("\n")

conn.interactive()

# AIS3{GGEZ!!LiNe42_COngRuen7i4l_6eNErATor}
