### HolyGrenade
- 給了一個pyc檔 廢話不說直接uncompile
- `$ uncompyle6 HolyGrenade.pyc > HolyGrenade.py`
- 得到`HolyGrenade.py`
```
from secret import flag
from hashlib import md5

def OO0o(arg):
    arg = bytearray(arg, 'ascii')
    for Oo0Ooo in range(0, len(arg), 4):
        O0O0OO0O0O0 = arg[Oo0Ooo]
        iiiii = arg[(Oo0Ooo + 1)]
        ooo0OO = arg[(Oo0Ooo + 2)]
        II1 = arg[(Oo0Ooo + 3)]
        arg[Oo0Ooo + 2] = II1
        arg[Oo0Ooo + 1] = O0O0OO0O0O0
        arg[Oo0Ooo + 3] = iiiii
        arg[Oo0Ooo] = ooo0OO
    return arg.decode('ascii')
    
flag += '0' * (len(flag) % 4)
for Oo0Ooo in range(0, len(flag), 4):
    print(OO0o(md5(bytes(flag[Oo0Ooo:Oo0Ooo + 4])).hexdigest()))
```
- 題目還給了output.txt
```
ba3a7f3bd92a5d418f5e16886db62674
33e4500b205b80e52dd52e796cba8b7d
7d1c09bbf2025facf6bd0fec0ec6a780
9cedd8dee7b5b87838d7a9bed76df8e5
764d30cb4807c5a870a47b53be6cf662
f1e8fda6c3ff87e43905ea1690624c64
d7939cb11edaa9b1fb05efb4e2946f75
5ae001ebd955475c867617bdb72e7728
```
- HolyGrenade把flag每4個字切成一個block 然後拿去做md5 得到output.txt
- flag的字元有限 可以直接暴力破解
```
import string
import itertools
from hashlib import md5

A = string.printable[:-5]

flag = u"""ba3a7f3bd92a5d418f5e16886db62674
33e4500b205b80e52dd52e796cba8b7d
7d1c09bbf2025facf6bd0fec0ec6a780
9cedd8dee7b5b87838d7a9bed76df8e5
764d30cb4807c5a870a47b53be6cf662
f1e8fda6c3ff87e43905ea1690624c64
d7939cb11edaa9b1fb05efb4e2946f75
5ae001ebd955475c867617bdb72e7728""".split(u"\n")

def OO0o(arg):
    arg = bytearray(arg, 'ascii')
    for Oo0Ooo in range(0, len(arg), 4):
        O0O0OO0O0O0 = arg[Oo0Ooo]
        iiiii = arg[(Oo0Ooo + 1)]
        ooo0OO = arg[(Oo0Ooo + 2)]
        II1 = arg[(Oo0Ooo + 3)]
        arg[Oo0Ooo + 2] = II1
        arg[Oo0Ooo + 1] = O0O0OO0O0O0
        arg[Oo0Ooo + 3] = iiiii
        arg[Oo0Ooo] = ooo0OO
    return arg.decode('ascii')

for i in itertools.product(A, repeat=4):
	j = ''.join(i)
	hash = OO0o(md5(bytes(j)).hexdigest())
	for index, value in enumerate(flag):
		if value == hash:
			flag[index] = j
            
print(u"".join(flag))
```
- flag: `AIS3{7here_15_the_k1ll3r_ra661t}`