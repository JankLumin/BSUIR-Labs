import logging
import os
import secrets
from typing import Optional, Tuple, List

PRIV_PATH = "priv.hex"
PUB_PATH = "pub.hex"
PLAIN_IN = "input.txt"
CIPHER_IO = "cipher.txt"
PLAIN_OUT = "output.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("ECC-ElGamal")

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

Point = Optional[Tuple[int, int]]
G: Point = (Gx, Gy)


def short_hex(b: bytes, take: int = 8) -> str:
    h = b.hex()
    return h if len(h) <= 2 * take else f"{h[:2*take]}…{h[-2*take:]}"


def short_int(x: int, take: int = 8) -> str:
    h = f"{x:0x}"
    return h if len(h) <= 2 * take else f"{h[:2*take]}…{h[-2*take:]}"


def is_on_curve(P: Point) -> bool:
    if P is None:
        return True
    x, y = P
    return (y * y - (x * x * x + a * x + b)) % p == 0


def mod_inv(x: int, m: int) -> int:
    return pow(x, -1, m)


def point_add(P: Point, Q: Point) -> Point:
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        if y1 == 0:
            return None
        s = (3 * x1 * x1 + a) * mod_inv(2 * y1 % p, p) % p
    else:
        if x1 == x2:
            return None
        s = (y2 - y1) * mod_inv((x2 - x1) % p, p) % p
    x3 = (s * s - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)


def point_neg(P: Point) -> Point:
    if P is None:
        return None
    x, y = P
    return (x, (-y) % p)


def point_mul(P: Point, k: int) -> Point:
    assert is_on_curve(P)
    if k % n == 0 or P is None:
        return None
    k %= n
    R = None
    Q = P
    while k:
        if k & 1:
            R = point_add(R, Q)
        Q = point_add(Q, Q)
        k >>= 1
    assert is_on_curve(R)
    return R


assert is_on_curve(G)


def mod_sqrt(a_: int) -> Optional[int]:
    a_ %= p
    if a_ == 0:
        return 0
    y = pow(a_, (p + 1) // 4, p)
    return y if (y * y - a_) % p == 0 else None


T = 256
BLOCK_DATA_BYTES = 30
BLOCK_TOTAL_BYTES = 31


def crc8(bs: bytes) -> int:
    crc = 0
    for b in bs:
        crc ^= b
        for _ in range(8):
            crc = ((crc << 1) ^ 0x07) & 0xFF if (crc & 0x80) else (crc << 1) & 0xFF
    return crc


def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, "big")


def int_to_bytes(x: int, length: int) -> bytes:
    return x.to_bytes(length, "big")


def encode_block_to_point(m: int) -> Point:
    assert 0 <= m < (p - 1) // T
    base = m * T
    j_max = min(T - 1, (p - 1) - base)
    for j in range(j_max + 1):
        x = base + j
        rhs = (pow(x, 3, p) + a * x + b) % p
        y = mod_sqrt(rhs)
        if y is not None:
            if y & 1:
                y = (-y) % p
            P = (x, y)
            assert is_on_curve(P)
            return P
    raise ValueError(
        "Не удалось закодировать блок в точку (уменьшите BLOCK_DATA_BYTES или увеличьте T)."
    )


def decode_point_to_block(P: Point) -> int:
    if P is None:
        raise ValueError("∞ не кодирует блок")
    x, _ = P
    return x // T


def chunk_bytes(data: bytes, size: int) -> List[bytes]:
    return [data[i : i + size] for i in range(0, len(data), size)]


def compress(P: Point) -> bytes:
    if P is None:
        return b"\x00"
    x, y = P
    prefix = 0x02 if (y % 2 == 0) else 0x03
    return bytes([prefix]) + x.to_bytes(32, "big")


def decompress(bts: bytes) -> Point:
    if bts == b"\x00":
        return None
    if len(bts) != 33 or bts[0] not in (2, 3):
        raise ValueError(
            "Неверный формат сжатой точки (ожидается 33 байта, префикс 0x02/0x03)"
        )
    prefix = bts[0]
    x = int.from_bytes(bts[1:], "big")
    rhs = (pow(x, 3, p) + a * x + b) % p
    y = mod_sqrt(rhs)
    if y is None:
        raise ValueError(
            "Не удаётся восстановить Y: точка не на кривой (возможна порча строки)."
        )
    if (y % 2 == 0 and prefix == 3) or (y % 2 == 1 and prefix == 2):
        y = (-y) % p
    P = (x, y)
    assert is_on_curve(P)
    return P


def generate_keypair() -> Tuple[int, Point]:
    while True:
        d = secrets.randbelow(n)
        if 1 <= d < n:
            Q = point_mul(G, d)
            if Q is not None:
                return d, Q


def encrypt_point(M: Point, Qpub: Point) -> Tuple[Point, Point]:
    if not is_on_curve(Qpub) or Qpub is None:
        raise ValueError("Публичный ключ некорректен")
    k = secrets.randbelow(n - 1) + 1
    C1 = point_mul(G, k)
    kQ = point_mul(Qpub, k)
    C2 = point_add(M, kQ)
    return C1, C2


def decrypt_point(C1: Point, C2: Point, d: int) -> Point:
    dC1 = point_mul(C1, d)
    return point_add(C2, point_neg(dC1))


def pairs_to_lines(pairs: List[Tuple[bytes, bytes]]) -> List[str]:
    return [f"{c1.hex()};{c2.hex()}" for c1, c2 in pairs]


def lines_to_pairs(lines: List[str]) -> List[Tuple[bytes, bytes]]:
    out: List[Tuple[bytes, bytes]] = []
    for idx, ln in enumerate(lines, 1):
        ln = ln.strip()
        if not ln:
            log.info("Строка %d пустая — пропущена", idx)
            continue
        if ";" not in ln:
            raise ValueError(f"Строка {idx}: отсутствует ';' между C1 и C2.")
        c1h, c2h = ln.split(";", 1)
        try:
            c1b = bytes.fromhex(c1h)
            c2b = bytes.fromhex(c2h)
        except ValueError as e:
            raise ValueError(f"Строка {idx}: невалидный hex: {e}")
        out.append((c1b, c2b))
    return out


def encrypt_bytes(plain: bytes, Qpub: Point) -> List[Tuple[bytes, bytes]]:
    payload = len(plain).to_bytes(4, "big") + plain

    blocks = chunk_bytes(payload, BLOCK_DATA_BYTES)
    log.info(
        "Этап шифрования: блоков %d (данных %d байт + CRC1 = %d байт на блок)",
        len(blocks),
        BLOCK_DATA_BYTES,
        BLOCK_TOTAL_BYTES,
    )

    pairs: List[Tuple[bytes, bytes]] = []
    for i, data_block in enumerate(blocks, 1):
        if len(data_block) < BLOCK_DATA_BYTES:
            data_block = data_block + b"\x00" * (BLOCK_DATA_BYTES - len(data_block))
        c = crc8(data_block)
        block_with_crc = data_block + bytes([c])

        m = bytes_to_int(block_with_crc)
        assert m < (p - 1) // T, "m слишком велик, уменьшите BLOCK_DATA_BYTES"

        Pm = encode_block_to_point(m)
        C1, C2 = encrypt_point(Pm, Qpub)
        pairs.append((compress(C1), compress(C2)))

        if i <= 3 or i == len(blocks):
            log.info(
                "  Блок %d/%d: CRC=%02x, m=%s -> C1=%s ; C2=%s",
                i,
                len(blocks),
                c,
                short_int(m),
                short_hex(compress(C1)),
                short_hex(compress(C2)),
            )
        elif i % 100 == 0:
            log.info("  … обработано %d блоков", i)
    return pairs


def decrypt_bytes(pairs: List[Tuple[bytes, bytes]], d: int) -> bytes:
    buf = bytearray()
    total = len(pairs)
    log.info("Этап дешифрования: пар %d", total)
    for i, (c1b, c2b) in enumerate(pairs, 1):
        try:
            C1 = decompress(c1b)
            C2 = decompress(c2b)
        except Exception as e:
            raise ValueError(f"Пара {i}: ошибка декомпрессии точек: {e}")
        if not is_on_curve(C1) or not is_on_curve(C2):
            raise ValueError(
                f"Пара {i}: точка(и) не на кривой (повреждение шифртекста)."
            )

        Pm = decrypt_point(C1, C2, d)
        if Pm is None or not is_on_curve(Pm):
            raise ValueError(f"Пара {i}: восстановленная точка сообщения некорректна.")

        m = decode_point_to_block(Pm)
        block_with_crc = int_to_bytes(m, BLOCK_TOTAL_BYTES)
        data_block = block_with_crc[:-1]
        c_stored = block_with_crc[-1]
        c_actual = crc8(data_block)
        if c_actual != c_stored:
            raise ValueError(
                f"Пара {i}: CRC mismatch (ожидалось {c_stored:02x}, вычислено {c_actual:02x})."
            )

        buf.extend(data_block)

        if i <= 3 or i == total:
            log.info(
                "  Пара %d/%d: C1=%s ; C2=%s -> CRC=%02x OK",
                i,
                total,
                short_hex(c1b),
                short_hex(c2b),
                c_stored,
            )
        elif i % 100 == 0:
            log.info("  … обработано %d пар", i)

    if len(buf) < 4:
        raise ValueError("Данные повреждены: нет 4-байтового префикса длины.")
    L = int.from_bytes(buf[:4], "big")
    data = bytes(buf[4 : 4 + L])
    if len(data) != L:
        raise ValueError(
            f"Некорректная длина при восстановлении: ожидалось {L}, получили {len(data)}."
        )
    log.info("Готово: полезная длина %d байт", L)
    return data


def save_priv_hex(path: str, d: int):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{d:064x}\n")


def save_pub_hex(path: str, Q: Point):
    with open(path, "w", encoding="utf-8") as f:
        f.write(compress(Q).hex() + "\n")


def load_priv_hex(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        s = f.read().strip()
    return int(s, 16)


def load_pub_hex(path: str) -> Point:
    with open(path, "r", encoding="utf-8") as f:
        s = f.read().strip()
    return decompress(bytes.fromhex(s))


def cmd_gen_keys():
    d, Q = generate_keypair()
    save_priv_hex(PRIV_PATH, d)
    save_pub_hex(PUB_PATH, Q)
    log.info("Сгенерированы ключи.")
    log.info("  priv: %s", f"{d:064x}")
    log.info("  pub : %s", compress(Q).hex())
    print("OK: создано priv.hex / pub.hex")


def cmd_encrypt():
    if not os.path.exists(PUB_PATH) or not os.path.exists(PRIV_PATH):
        log.info("Ключи не найдены — генерируем…")
        cmd_gen_keys()
    Q = load_pub_hex(PUB_PATH)
    d = load_priv_hex(PRIV_PATH)
    log.info("Ключи загружены. priv=%s…, pub=%s…", short_int(d), short_hex(compress(Q)))
    if not os.path.exists(PLAIN_IN):
        with open(PLAIN_IN, "w", encoding="utf-8") as f:
            f.write("Привет, это тестовое сообщение!")
        log.info("Создан тестовый %s", PLAIN_IN)
    with open(PLAIN_IN, "r", encoding="utf-8") as f:
        data = f.read().encode("utf-8")
    log.info("Читаем %s: %d байт", PLAIN_IN, len(data))
    pairs = encrypt_bytes(data, Q)
    lines = pairs_to_lines(pairs)
    with open(CIPHER_IO, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    log.info("Шифртекст записан в %s: %d строк", CIPHER_IO, len(lines))
    print(f"OK: {PLAIN_IN} -> {CIPHER_IO}")


def cmd_decrypt():
    if not os.path.exists(PRIV_PATH):
        raise SystemExit(
            "Нет приватного ключа priv.hex. Сначала запусти gen-keys/encrypt."
        )
    d = load_priv_hex(PRIV_PATH)
    log.info("Загружен приватный ключ: %s…", short_int(d))
    if not os.path.exists(CIPHER_IO):
        raise SystemExit(f"Нет {CIPHER_IO}. Сначала запусти encrypt.")
    with open(CIPHER_IO, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    log.info("Читаем %s: %d строк", CIPHER_IO, len(lines))
    pairs = lines_to_pairs(lines)
    plain = decrypt_bytes(pairs, d)
    try:
        text = plain.decode("utf-8")
        preview = text[:80].replace("\n", "\\n")
        with open(PLAIN_OUT, "w", encoding="utf-8") as f:
            f.write(text)
        log.info("Расшифрованный UTF-8 записан в %s", PLAIN_OUT)
        log.info('Превью: "%s"%s', preview, "…" if len(text) > 80 else "")
    except UnicodeDecodeError:
        with open(PLAIN_OUT, "wb") as f:
            f.write(plain)
        log.info("Расшифрованные байты (не UTF-8) записаны в %s", PLAIN_OUT)
        log.info("Превью HEX: %s", short_hex(plain))
    print(f"OK: {CIPHER_IO} -> {PLAIN_OUT}")


def main():
    import sys

    if len(sys.argv) != 2 or sys.argv[1] not in ("gen-keys", "encrypt", "decrypt"):
        print("Использование:")
        print("  python main.py gen-keys   создать priv.hex/pub.hex")
        print("  python main.py encrypt    input.txt -> cipher.txt")
        print("  python main.py decrypt    cipher.txt -> output.txt")
        raise SystemExit(1)
    cmd = sys.argv[1]
    if cmd == "gen-keys":
        cmd_gen_keys()
    elif cmd == "encrypt":
        cmd_encrypt()
    elif cmd == "decrypt":
        cmd_decrypt()


if __name__ == "__main__":
    main()
