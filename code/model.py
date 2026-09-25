"""Independent review model for ordinary FEILIAN conformance checks.

Not a production hash library. The C profile follows the supplied scalar/SIMD
code; chapter2 uses the printed IV and AddConstant rows, little-endian message
words, and high-word-first counter. This choice is stated, not declared canonical.
"""

MASK = (1 << 64) - 1
IV_C = tuple(int(x, 16) for x in (
    '243f6a8885a308d3 13198a2e03707344 a4093822299f31d0 082efa98ec4e6c89 '
    '452821e638d01377 be5466cf34e90c6c c0ac29b7c97c50dd 3f84d5b5b5470917 '
    '9216d5d98979fb1b d1310ba698dfb5ac 2ffd72dbd01adfb7 b8e1afed6a267e96 '
    'ba7c9045f12c7f99 24a19947b3916cf7 0801f2e2858efc16 636920d871574e69'
).split())
IV_CH2 = IV_C[:7] + (0x3D84D5B5B5470917,) + IV_C[8:]
CONSTANTS = (0x6A09E667F3BCC908, 0xBB67AE8584CAA73B,
             0x3C6EF372FE94F82B, 0xA54FF53A5F1D36F1)


def ror(x, n):
    return ((x >> n) | (x << (64 - n))) & MASK


def sigma0(x):
    return x ^ ror(x, 5) ^ ror(x, 48)


def sigma1(x):
    return x ^ ror(x, 11) ^ ror(x, 40)


def subcolumn(a, b, c, d):
    a = (a + b) & MASK
    c = (c + d) & MASK
    d = ror(d ^ a, 8)
    c = (c + sigma0(d)) & MASK
    b = ror(b ^ c, 63)
    a = (a + sigma1(b)) & MASK
    return a, b, c, d


def inverse_subcolumn(a, b, c, d):
    """The inverse printed in section 4.5.2, for a bijectivity check."""
    ab = (a - sigma1(b)) & MASK
    old_b = c ^ ror(b, 1)
    cd = (c - sigma0(d)) & MASK
    old_d = ab ^ ror(d, 56)
    return (ab - old_b) & MASK, old_b, (cd - old_d) & MASK, old_d


def half_round(v):
    w = list(v)
    for col in range(4):
        words = subcolumn(*(v[col + 4*r] for r in range(4)))
        for r in range(4):
            w[col + 4*r] = words[r]
    return [w[4*r + (col + r) % 4] for r in range(4) for col in range(4)]


def compress(h, message_words, version, final, bit_count, profile):
    v = list(h)
    tweak = (version, MASK if final else 0, bit_count >> 64, bit_count & MASK)
    for rnd in range(20):
        for half in range(2):
            if rnd % 4 == 0:
                base = 8 * half
                for col in range(4):
                    v[col] ^= message_words[base + col]
                    v[8 + col] ^= message_words[base + 4 + col]
            v = half_round(v)
        constants = [CONSTANTS[(rnd//4 + i) % 4] for i in range(4)]
        row1, row3 = (constants, tweak) if profile == 'c' else (tweak, constants)
        for i in range(4):
            v[4 + i] ^= row1[i]
            v[12 + i] ^= row3[i]
    return tuple(a ^ b for a, b in zip(h, v))


def hash_model(message, bits, digest_bits, profile='c'):
    if digest_bits not in (512, 768, 1024) or profile not in ('c', 'chapter2'):
        raise ValueError('Not a supported named profile')
    if not 0 <= bits < (1 << 128) or bits > 8 * len(message):
        raise ValueError('Message does not contain the requested bits')
    nbytes = (bits + 7) // 8
    message = bytearray(message[:nbytes])
    if bits % 8:
        message[-1] &= (0xff << (8 - bits % 8)) & 0xff
    nblocks = max(1, (bits + 1023) // 1024)
    message.extend(bytes(nblocks * 128 - nbytes))
    h = IV_C if profile == 'c' else IV_CH2
    for i in range(nblocks):
        block = message[128*i:128*(i+1)]
        words = tuple(int.from_bytes(block[j:j+8], 'little') for j in range(0, 128, 8))
        h = compress(h, words, digest_bits, i == nblocks-1,
                     min(1024*(i+1), bits), profile)
    return b''.join(x.to_bytes(8, 'little') for x in h)[:digest_bits//8]



def linear_rank(function):
    pivots = {}
    for i in range(64):
        x = function(1 << i)
        while x:
            bit = x.bit_length()-1
            if bit in pivots:
                x ^= pivots[bit]
            else:
                pivots[bit] = x
                break
    return len(pivots)

