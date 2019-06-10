#!/usr/bin/env python3.7
import os

BLOCK_SIZE = 256

P = [
    (0, [1, 7]),
    (1, [0, 8]),
    (0, [5, 3]),
    (1, [8, 6]),
    (0, [3, 9]),
    (1, [4, 0]),
    (0, [9, 1]),
    (1, [6, 2]),
    (0, [7, 5]),
    (1, [2, 4]),
]

def n2B(b,length=BLOCK_SIZE):
    return list(map(int, bin(b)[2:].rjust(BLOCK_SIZE, '0')))

def B2n(b):
    return int("".join(map(str, b)), 2)

def swap(b):
    l = BLOCK_SIZE // 2
    mask = (1 << l) - 1
    return (b >> l) | ((b & mask) << l)

def bitchain(cb, state=0):
    if len(cb) == 0: 
        return cb
    b, ns = P[state]
    b0, bn = cb[0],cb[1:]
    return [b0 ^ b] + bitchain(bn, state=ns[b0])

def blockcipher(b):
    return B2n(bitchain(n2B(b)))

class CbC:

    def __init__(self, k, rounds):
        self.key = [k]
        self.rounds = rounds
        for i in range(1, self.rounds):
            k = swap(blockcipher(k))
            self.key.append(k)

    def encrypt(self, b):
        for i in range(self.rounds):
            b ^= self.key[i]
            b = swap(blockcipher(b))
        return b

    def decrypt(self, b):
        for i in range(self.rounds)[::-1]:
            b = swap(blockcipher(b))
            b ^= self.key[i]
        return b

def solve():
    pt2, ct2 = (76173805501177359573786250867826865667623985658852407459502964711159068527937, 7132216118997241161329301114592304948838945360663660382939528954550389872641)
    flag = CbC(pt2, 99).decrypt(ct2)
    print("Flag : AIS3{%s}" % hex(flag)[2:])

if __name__ == "__main__":
    pt1 = int(bytes.hex(os.urandom(BLOCK_SIZE // 8)), 16)
    pt2 = int(bytes.hex(os.urandom(BLOCK_SIZE // 8)), 16)

    C1 = CbC(pt1, 99)
    C2 = CbC(pt2, 99)

    ct1 = C1.encrypt(pt2)
    ct2 = C2.encrypt(pt1)

    print(pt1, ct1)
    print(pt2, ct2)
    print(C1.decrypt(ct1))

    solve()
