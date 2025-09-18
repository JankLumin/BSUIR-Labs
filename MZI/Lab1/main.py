import sys
import struct

BLOCK_SIZE = 8
KEY_SIZE = 32

KEY_HEX = "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F"
KEY = bytes.fromhex(KEY_HEX)

SBOX_HEX = """
04 0A 09 02 0D 08 00 0E 06 0B 01 0C 07 0F 05 03
0E 0B 04 0C 06 0D 0F 0A 02 03 08 01 00 07 05 09
05 08 01 0D 0A 03 04 02 0E 0F 0C 07 06 00 09 0B
07 0D 0A 01 00 08 09 0F 0E 04 06 0C 0B 02 05 03
06 0C 07 01 05 0F 0D 08 04 0A 09 0E 00 03 0B 02
04 0B 0A 00 07 02 01 0D 03 06 08 05 09 0C 0F 0E
0D 0B 04 01 03 0F 05 09 00 0A 0E 07 06 08 02 0C
01 0F 0D 00 05 07 0A 04 09 02 03 0E 06 0B 08 0C
""".strip()
SBOX_BYTES = bytes.fromhex(" ".join(SBOX_HEX.split()))


def rotl32(x, n):
    x &= 0xFFFFFFFF
    n &= 31
    return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))


def substitute(x):
    out = 0
    for i in range(8):
        nib = (x >> (4 * i)) & 0xF
        sb = SBOX_BYTES[i * 16 + nib] & 0xF
        out |= sb << (4 * i)
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
            print(f"Раунд {r+1:2d}: N1=0x{n1:08X}, N2=0x{n2:08X}")
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
            print(f"Раунд {r+1:2d}: N1=0x{n1:08X}, N2=0x{n2:08X}")
    return join_block(n2, n1)


def pad(data):
    padlen = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    if padlen == 0:
        padlen = BLOCK_SIZE
    print(f"[PKCS7] +{padlen} байт")
    return data + bytes([padlen]) * padlen


def unpad(data):
    if not data or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Некорректная длина для PKCS#7.")
    p = data[-1]
    print(f"[PKCS7] last=0x{p:02X}")
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
            f"\nБлок {i//BLOCK_SIZE:02d} (ENC) IN: {blk.hex().upper()}  '{safe_ascii(blk)}'"
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
        print(f"\nБлок {i//BLOCK_SIZE:02d} (DEC) IN: {blk.hex().upper()}")
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
        print(f"\nШифртекст (HEX) записан в: {out_path}")
    else:
        hextext = open(in_path, "r", encoding="utf-8").read()
        plain = decrypt_text(hextext)
        open(out_path, "w", encoding="utf-8").write(plain)
        print(f"\nРасшифрованный текст записан в: {out_path}")


if __name__ == "__main__":
    main()
