import numpy as np

SBOX = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

P = [ 0, 16, 32, 48,  1, 17, 33, 49,  2, 18, 34, 50,  3, 19, 35, 51,
      4, 20, 36, 52,  5, 21, 37, 53,  6, 22, 38, 54,  7, 23, 39, 55,
      8, 24, 40, 56,  9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
     12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]


def generate_round_keys(key):
    keys = [key]
    k = key
    for i in range(1, 32):
        k = (k >> 19) | ((k << 61) & 0xffffffffffffffffffff)
        head = (k >> 76) & 0xf
        k = (k & 0xfffffffffffffffffff) | (SBOX[head] << 76)
        k ^= i << 15
        keys.append(k)
    return keys


def add_round_key(state, key):
    return state ^ (key >> 16)


def sbox_layer(state):
    result = 0
    for i in range(16):
        result |= SBOX[(state >> (4 * i)) & 0xf] << (4 * i)
    return result


def p_layer(state):
    result = 0
    for i in range(64):
        result |= ((state >> i) & 1) << P[i]
    return result


def encrypt(plaintext, keys):
    state = plaintext
    for i in range(31):
        state = add_round_key(state, keys[i])
        state = sbox_layer(state)
        state = p_layer(state)
    return add_round_key(state, keys[31])


def build_ddt(sbox):
    n = len(sbox)
    ddt = np.zeros((n, n), dtype=int)
    for a in range(n):
        for x in range(n):
            ddt[a][sbox[x] ^ sbox[x ^ a]] += 1
    return ddt


DDT = build_ddt(SBOX)


def validate_trail(deltas, R):
    for r in range(R):
        din, dout = deltas[r], deltas[r + 1]
        for s in range(16):
            in_nib  = (din >> (4 * s)) & 0xF
            out_nib = sum(((dout >> P[4 * s + j]) & 1) << j for j in range(4))
            if DDT[in_nib][out_nib] == 0:
                return False
    return True
