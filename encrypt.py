from random import randint
from base64 import b64decode

class Crypt:
    def __init__(self, key):
        self.key = key

    def crypt(self):
        pass

    def decrypt(self):
        pass


def egcd(a, b):
    if b == 0:
        return 1, 0
    else:
        x, y = egcd(b, a % b)
        return y, x - y * (a // b)


def rmspp(number, attempts=28):
    s = number // 2
    r = 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for att in range(attempts):
        a = mod_exp(randint(2, number - 2), s, number)
        if a not in (1, number - 1):
            for j in range(r):
                if mod_exp(a, 2**j, number) == number - 1:
                    break
            else:
                return False
    return True


def mod_exp(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if (exponent & 1) == 1:
            result = (result * base) % modulus
        exponent >>= 1
        base = (base * base) % modulus
    return result


def decrypt(dk, crypt_token):
    p = sum([dk.encode()[-i-1]*256**i for i in range(len(dk.encode()))]) | 1
    p **= 2
    while not rmspp(p):
        p += 2
    q = p + 2
    while not rmspp(q):
        q += 2
    n = p * q
    phi = (p - 1) * (q - 1)
    d = egcd(phi, 65537)[1] + phi
    nk = int(''.join([bin(i)[2:].rjust(8, '0') for i in b64decode(crypt_token)]), 2)
    m = mod_exp(nk, d, n)
    bin_m = bin(m)[2:].rjust(35 * 8, '0')
    k = ''.join([chr(int(bin_m[i: i + 8], 2)) for i in range(0, 280, 8)])
    def wrap(func):
        def f(*argv, **kwargs):
            return func(*argv, **kwargs, token=k)
        return f
    return wrap