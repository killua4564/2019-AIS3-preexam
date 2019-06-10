import base64
import itertools

def toBin(s):
    ret = []
    if type(s) == type(b''):
        s = "".join(map(chr, s))
    for c in s:
        ret.append(bin(ord(c))[2:].zfill(8))
    return "".join(ret)

class LFSR:

    def __init__(self, register, taps):
        self.register = register
        self.taps = taps

    def next(self):
        ret = self.register[0]
        new = 0
        for i in self.taps:
            new ^= self.register[i]
        self.register.append(new)
        self.register = self.register[1:]
        return ret

with open('fake.png','rb') as f:
    flag = f.read()[:6]
    flag = base64.b64encode(flag)
    binary = toBin(flag)
    print(binary)

with open('enc.png', 'rb') as f:
    enc = f.read()
    enc_binary = bin(int(str(enc, "utf-8"), 16))[2:]
    print(enc_binary[:64])

register_header = []
for i, j in zip(binary, enc_binary):
    register_header.append(int(i) ^ int(j))

print(''.join(map(str, register_header)))

# for n in range(2, 16):
#     for i in itertools.combinations(list(range(16)), n):
#         key = True
#         lfsr = LFSR(register_header[:16], list(i))

#         for bit in register_header:
#             if bit != lfsr.next():
#                 key = False
#                 break
        
#         if key: print(list(i))

taps = [2, 3, 5, 11, 12]
lfsr = LFSR(register_header[:16], taps)

dec = ""
for b in enc_binary:
    dec += str(int(b) ^ lfsr.next())

dec_base64 = []
for i in range(0, len(dec), 8):
    dec_base64.append(int(dec[i:i+8], 2))

open("flag.png", "wb").write(base64.b64decode(bytes(dec_base64)))

