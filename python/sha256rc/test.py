from hashlib import sha256
from binascii import hexlify

inputs = [
    b"FOO-0x000000003B1BD2039" + b" " * 53 + b"\xdd\x3f\xf4\x6f",
    b"BAR-0x00000000307238E22" + b" " * 53 + b"\xa8\x0d\xa3\x23",
    b"FOOBAR-0x000000001BB6C4C9F" + b" " * 50 + b"\xb0\x1d\x7c\x21"
]

h = [sha256(sha256(x).digest()).digest() for x in inputs]
xor = bytes([h[0][i] ^ h[1][i] ^ h[2][i] for i in range(32)])

print('  sha256({})'.format(sha256(inputs[0]).hexdigest()))
print('^ sha256({})'.format(sha256(inputs[1]).hexdigest()))
print('^ sha256({})'.format(sha256(inputs[2]).hexdigest()))
print(' =====================================================')
print(' {}'.format(hexlify(xor).decode()))
