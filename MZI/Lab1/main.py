import sys
import struct

BLOCK_SIZE = 8
KEY_SIZE = 32

SBOX = [
    [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
    [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
    [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
    [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
    [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
    [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
    [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
    [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12],
]

KEY = bytes(range(32))


def rotl32(x, n):
    x &= 0xFFFFFFFF
    return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))


def substitute(x):
    out = 0
    for i in range(8):
        nib = (x >> (4 * i)) & 0xF
        out |= (SBOX[i][nib] & 0xF) << (4 * i)
    return out


def split_block(b):
    return struct.unpack(">II", b)


def join_block(n1, n2):
    return struct.pack(">II", n1 & 0xFFFFFFFF, n2 & 0xFFFFFFFF)


def key_schedule_enc(key):
    k = struct.unpack(">IIIIIIII", key)
    sched = []
    for _ in range(3):
        sched.extend(k)
    sched.extend(reversed(k))
    return sched


def key_schedule_dec(key):
    return list(reversed(key_schedule_enc(key)))


def encrypt_block(block, key, trace=False):
    n1, n2 = split_block(block)
    ks = key_schedule_enc(key)
    for r in range(32):
        f = (n2 + ks[r]) & 0xFFFFFFFF
        f = substitute(f)
        f = rotl32(f, 11)
        n1, n2 = n2, (n1 ^ f) & 0xFFFFFFFF
        if trace:
            print(f"main.py | Раунд {r+1:2d}: N1=0x{n1:08X}, N2=0x{n2:08X}")
    return join_block(n2, n1)


def decrypt_block(block, key, trace=False):
    n1, n2 = split_block(block)
    ks = key_schedule_dec(key)
    for r in range(32):
        f = (n2 + ks[r]) & 0xFFFFFFFF
        f = substitute(f)
        f = rotl32(f, 11)
        n1, n2 = n2, (n1 ^ f) & 0xFFFFFFFF
        if trace:
            print(f"main.py | Раунд {r+1:2d}: N1=0x{n1:08X}, N2=0x{n2:08X}")
    return join_block(n2, n1)


def pad(data):
    padlen = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    if padlen == 0:
        padlen = BLOCK_SIZE
    return data + bytes([padlen]) * padlen


def unpad(data):
    if not data or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Некорректная длина для PKCS#7.")
    p = data[-1]
    if p < 1 or p > BLOCK_SIZE or data[-p:] != bytes([p]) * p:
        raise ValueError("Некорректная добивка PKCS#7.")
    return data[:-p]


def safe_ascii(b):
    return "".join(chr(x) if 32 <= x <= 126 else "." for x in b)


def encrypt_text(text):
    data = text.encode("utf-8")
    data = pad(data)
    out = bytearray()
    for i in range(0, len(data), BLOCK_SIZE):
        blk = data[i : i + BLOCK_SIZE]
        print(
            f"\nmain.py | Блок {i//BLOCK_SIZE:02d} (ENC) IN: {blk.hex().upper()}  '{safe_ascii(blk)}'"
        )
        out += encrypt_block(blk, KEY, trace=True)
    return out.hex().upper()


def decrypt_text(hextext):
    hex_clean = "".join(ch for ch in hextext if ch.strip())
    if len(hex_clean) % 2 != 0:
        raise ValueError("Нечетная длина HEX — поврежденный шифртекст?")
    data = bytes.fromhex(hex_clean)
    out = bytearray()
    for i in range(0, len(data), BLOCK_SIZE):
        blk = data[i : i + BLOCK_SIZE]
        print(f"\nmain.py | Блок {i//BLOCK_SIZE:02d} (DEC) IN: {blk.hex().upper()}")
        out += decrypt_block(blk, KEY, trace=True)
    return unpad(bytes(out)).decode("utf-8")


def usage():
    print("Использование: python main.py encrypt(decrypt) in.txt out.txt")


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ("encrypt", "decrypt"):
        usage()
        return
    mode, in_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

    if mode == "encrypt":
        text = open(in_path, "r", encoding="utf-8").read()
        cipher_hex = encrypt_text(text)
        open(out_path, "w", encoding="utf-8").write(cipher_hex)
        print(f"\nmain.py | Шифртекст (HEX) записан в: {out_path}")
    else:
        hextext = open(in_path, "r", encoding="utf-8").read()
        plain = decrypt_text(hextext)
        open(out_path, "w", encoding="utf-8").write(plain)
        print(f"\nmain.py | Расшифрованный текст записан в: {out_path}")


if __name__ == "__main__":
    main()
