import sys, argparse, binascii

BLOCK = 16
KEY_HEX = "00112233445566778899AABBCCDDEEFF0F1E2D3C4B5A69788796A5B4C3D2E1F0"
IV_HEX = "A1B2C3D4E5F60718293A4B5C6D7E8F90"
KEY = binascii.unhexlify(KEY_HEX)
IV = binascii.unhexlify(IV_HEX)

H_HEX = (
    "B1 94 BA C8 0A 08 F5 3B 36 6D 00 8E 58 4A 5D E4"
    " 85 04 FA 9D 1B B6 C7 AC 25 2E 72 C2 02 FD CE 0D"
    " 5B E3 D6 12 17 B9 61 81 FE 67 86 AD 71 6B 89 0B"
    " 5C B0 C0 FF 33 C3 56 B8 35 C4 05 AE D8 E0 7F 99"
    " E1 2B DC 1A E2 82 57 EC 70 3F CC F0 95 EE 8D F1"
    " C1 AB 76 38 9F E6 78 CA F7 C6 F8 60 D5 BB 9C 4F"
    " F3 3C 65 7B 63 7C 30 6A DD 4E A7 79 9E B2 3D 31"
    " 3E 98 B5 6E 27 D3 BC CF 59 1E 18 1F 4C 5A B7 93"
    " E9 DE E7 2C 8F 0C 0F A6 2D DB 49 F4 6F 73 96 47"
    " 06 07 53 16 ED 24 7A 37 39 CB A3 83 03 A9 8B F6"
    " 92 BD 9B 1C E5 D1 41 01 54 45 FB C9 5E 4D 0E F2"
    " 68 20 80 AA 22 7D 64 2F 26 87 F9 34 90 40 55 11"
    " BE 32 97 13 43 FC 9A 48 A0 2A 88 5F 19 4B 09 A1"
    " 7E CD A4 D0 15 44 AF 8C A5 84 50 BF 66 D2 E8 8A"
    " A2 D7 46 52 42 A8 DF B3 69 74 C5 51 EB 23 29 21"
    " D4 EF D9 B4 3A 62 28 75 91 14 10 EA 77 6C DA 1D"
)
H_BYTES = binascii.unhexlify(H_HEX.replace(" ", ""))


def pkcs7_pad(b):
    n = BLOCK - (len(b) % BLOCK)
    if n == 0:
        n = BLOCK
    print(f"[PKCS7] +{n} байт")
    return b + bytes([n]) * n


def pkcs7_unpad(b):
    n = b[-1]
    print(f"[PKCS7] last=0x{n:02X}")
    if n < 1 or n > BLOCK or b[-n:] != bytes([n]) * n:
        raise ValueError("PKCS#7 error")
    return b[:-n]


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def _b2l16(b):
    return list(b)


def _l2b16(l):
    return bytes(l)


def _hex(b):
    return b.hex().upper()


def _ascii(b):
    return "".join(chr(x) if 32 <= x <= 126 else "." for x in b)


class STB:
    def __init__(self, key_bytes):
        self.Hb = H_BYTES
        kw = [self._list_to_int(key_bytes[i : i + 4]) for i in range(0, 32, 4)]
        self.k = [kw[i % 8] for i in range(56)]

    def _int_to_list(self, x):
        return [(x >> i) & 0xFF for i in (24, 16, 8, 0)]

    def _list_to_int(self, xs):
        sh = (24, 16, 8, 0)
        return (xs[0] << sh[0]) | (xs[1] << sh[1]) | (xs[2] << sh[2]) | (xs[3] << sh[3])

    def _rev(self, x):
        l = self._int_to_list(x)
        l.reverse()
        return self._list_to_int(l)

    def _rotl32(self, v, k):
        k &= 31
        v &= 0xFFFFFFFF
        return ((v << k) & 0xFFFFFFFF) | (v >> (32 - k))

    def _modadd(self, *vals):
        s = 0
        for el in vals:
            s = (s + self._rev(el)) & 0xFFFFFFFF
        return self._rev(s)

    def _modsub(self, x, y):
        return (x - y) & 0xFFFFFFFF

    def _H(self, x):
        return self.Hb[x]

    def _G(self, x, r):
        t = self._list_to_int([self._H(b) for b in self._int_to_list(x)])
        return self._rev(self._rotl32(self._rev(t), r))

    def encryption(self, m, trace=False):
        a, b, c, d = [self._list_to_int(m[i : i + 4]) for i in range(0, 16, 4)]
        if trace:
            print(f"  init: a={a:08X} b={b:08X} c={c:08X} d={d:08X}")
        for i in range(8):
            b ^= self._G(self._modadd(a, self.k[7 * i + 0]), 5)
            c ^= self._G(self._modadd(d, self.k[7 * i + 1]), 21)
            a = self._rev(
                self._modsub(
                    self._rev(a),
                    self._rev(self._G(self._modadd(b, self.k[7 * i + 2]), 13)),
                )
            )
            e = (self._G(self._modadd(b, c, self.k[7 * i + 3]), 21)) ^ self._rev(i + 1)
            b = self._modadd(b, e)
            c = self._rev(self._modsub(self._rev(c), self._rev(e)))
            d = self._modadd(d, self._G(self._modadd(c, self.k[7 * i + 4]), 13))
            b ^= self._G(self._modadd(a, self.k[7 * i + 5]), 21)
            c ^= self._G(self._modadd(d, self.k[7 * i + 6]), 5)
            a, b = b, a
            c, d = d, c
            b, c = c, b
            if trace:
                print(f"  rnd {i+1:02d}: a={a:08X} b={b:08X} c={c:08X} d={d:08X}")
        out = (
            self._int_to_list(b)
            + self._int_to_list(d)
            + self._int_to_list(a)
            + self._int_to_list(c)
        )
        if trace:
            oa, ob, oc, od = [
                self._list_to_int(out[i : i + 4]) for i in range(0, 16, 4)
            ]
            print(f"   out: a'={oa:08X} b'={ob:08X} c'={oc:08X} d'={od:08X}")
        return out

    def decryption(self, m, trace=False):
        a, b, c, d = [self._list_to_int(m[i : i + 4]) for i in range(0, 16, 4)]
        if trace:
            print(f"  init(dec): a={a:08X} b={b:08X} c={c:08X} d={d:08X}")
        for i in reversed(range(8)):
            b ^= self._G(self._modadd(a, self.k[7 * i + 6]), 5)
            c ^= self._G(self._modadd(d, self.k[7 * i + 5]), 21)
            a = self._rev(
                self._modsub(
                    self._rev(a),
                    self._rev(self._G(self._modadd(b, self.k[7 * i + 4]), 13)),
                )
            )
            e = (self._G(self._modadd(b, c, self.k[7 * i + 3]), 21)) ^ self._rev(i + 1)
            b = self._modadd(b, e)
            c = self._rev(self._modsub(self._rev(c), self._rev(e)))
            d = self._modadd(d, self._G(self._modadd(c, self.k[7 * i + 2]), 13))
            b ^= self._G(self._modadd(a, self.k[7 * i + 1]), 21)
            c ^= self._G(self._modadd(d, self.k[7 * i + 0]), 5)
            a, b = b, a
            c, d = d, c
            a, d = d, a
            if trace:
                print(f"  rnd {8-i:02d}: a={a:08X} b={b:08X} c={c:08X} d={d:08X}")
        out = (
            self._int_to_list(c)
            + self._int_to_list(a)
            + self._int_to_list(d)
            + self._int_to_list(b)
        )
        if trace:
            oa, ob, oc, od = [
                self._list_to_int(out[i : i + 4]) for i in range(0, 16, 4)
            ]
            print(f"   out(dec): a''={oa:08X} b''={ob:08X} c''={oc:08X} d''={od:08X}")
        return out


def enc_block(b):
    stb = STB(KEY)
    print(f"  ENC IN : { _hex(b) }  '{ _ascii(b) }'")
    out = stb.encryption(_b2l16(b), trace=True)
    outb = _l2b16(out)
    print(f"  ENC OUT: { _hex(outb) }")
    return outb


def dec_block(b):
    stb = STB(KEY)
    print(f"  DEC IN : { _hex(b) }")
    out = stb.decryption(_b2l16(b), trace=True)
    outb = _l2b16(out)
    print(f"  DEC OUT: { _hex(outb) }  '{ _ascii(outb) }'")
    return outb


def ecb_encrypt(data):
    print(f"[ECB] Шифрование: {len(data)} байт")
    data = pkcs7_pad(data)
    out = bytearray()
    for i in range(0, len(data), BLOCK):
        print(f"\n[ECB] Блок {i//BLOCK:02d}")
        out += enc_block(data[i : i + BLOCK])
    return bytes(out)


def ecb_decrypt(ct):
    if len(ct) % BLOCK != 0:
        raise ValueError("ECB: длина не кратна 16")
    print(f"[ECB] Расшифрование: {len(ct)} байт, блоков: {len(ct)//BLOCK}")
    out = bytearray()
    for i in range(0, len(ct), BLOCK):
        print(f"\n[ECB] Блок {i//BLOCK:02d}")
        out += dec_block(ct[i : i + BLOCK])
    print("\n[ECB] Снятие PKCS#7…")
    return pkcs7_unpad(bytes(out))


def cfb_encrypt(data, iv):
    print(f"[CFB] Шифрование: {len(data)} байт, IV={IV_HEX}")
    out = bytearray()
    fb = iv
    for i in range(0, len(data), BLOCK):
        print(f"\n[CFB-ENC] Блок {i//BLOCK:02d}")
        ks = enc_block(fb)
        chunk = data[i : i + BLOCK]
        y = xor_bytes(chunk, ks[: len(chunk)])
        print(f"   KS : { _hex(ks[:len(chunk)]) }")
        print(f"   IN : { _hex(chunk) }  '{ _ascii(chunk) }'")
        print(f"   OUT: { _hex(y) }")
        out += y
        fb = y if len(y) == 16 else (y + fb[len(y) :])
    return bytes(out)


def cfb_decrypt(ct, iv):
    print(f"[CFB] Расшифрование: {len(ct)} байт, IV={IV_HEX}")
    out = bytearray()
    fb = iv
    for i in range(0, len(ct), BLOCK):
        print(f"\n[CFB-DEC] Блок {i//BLOCK:02d}")
        ks = enc_block(fb)
        chunk = ct[i : i + BLOCK]
        x = xor_bytes(chunk, ks[: len(chunk)])
        print(f"   KS : { _hex(ks[:len(chunk)]) }")
        print(f"   IN : { _hex(chunk) }")
        print(f"   OUT: { _hex(x) }  '{ _ascii(x) }'")
        out += x
        fb = chunk if len(chunk) == 16 else (chunk + fb[len(chunk) :])
    return bytes(out)


def main():
    p = argparse.ArgumentParser(
        description="СТБ 34.101.31-2011: ECB/CFB (хардкод, трейс)"
    )
    p.add_argument("action", choices=["encrypt", "decrypt"])
    p.add_argument("mode", choices=["ecb", "cfb"])
    p.add_argument("inp")
    p.add_argument("out")
    args = p.parse_args()

    with open(args.inp, "rb") as f:
        data = f.read()
    print(
        f"[INFO] action={args.action} mode={args.mode} in={args.inp}({len(data)}B) key={KEY_HEX} iv={IV_HEX}"
    )

    if args.mode == "ecb":
        res = ecb_encrypt(data) if args.action == "encrypt" else ecb_decrypt(data)
    else:
        res = (
            cfb_encrypt(data, IV) if args.action == "encrypt" else cfb_decrypt(data, IV)
        )

    with open(args.out, "wb") as f:
        f.write(res)
    print(f"\n[OK] saved -> {args.out} ({len(res)}B)")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Использование: python main.py encrypt(decrypt) ecb(cfb) in.txt out.txt")
        sys.exit(2)
    main()
