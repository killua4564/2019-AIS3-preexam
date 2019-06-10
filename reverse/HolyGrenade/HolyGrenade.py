# uncompyle6 version 3.3.3
# Python bytecode 3.7 (3394)
# Decompiled from: Python 2.7.16 (default, Mar  4 2019, 09:01:38) 
# [GCC 4.2.1 Compatible Apple LLVM 10.0.0 (clang-1000.11.45.5)]
# Embedded file name: HolyGrenade.py
# Size of source mod 2**32: 829 bytes
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
# okay decompiling HolyGrenade.pyc
