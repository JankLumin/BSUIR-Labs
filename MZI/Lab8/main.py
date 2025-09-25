import logging
import os
import sys
import math
import warnings
import numpy as np
from PIL import Image

warnings.filterwarnings("ignore", message=".*'mode' parameter is deprecated.*")

INPUT_TXT = "input.txt"
COVER_JPG = "cover.jpg"
STEGO_JPG = "stego.jpg"
OUTPUT_TXT = "output.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("JPEG-Stego")

BLOCK = 8
CHANNEL_IDX = 0
COEF_POS = (4, 3)
QUALITY = 75

QY = np.array(
    [
        [8, 6, 5, 8, 12, 20, 26, 31],
        [6, 6, 7, 10, 13, 29, 30, 28],
        [7, 7, 8, 12, 20, 29, 35, 28],
        [7, 9, 12, 15, 26, 44, 40, 31],
        [9, 12, 19, 28, 34, 55, 52, 39],
        [12, 18, 28, 32, 41, 52, 57, 46],
        [25, 32, 39, 44, 52, 61, 60, 51],
        [36, 46, 48, 49, 56, 50, 52, 50],
    ],
    dtype=np.int32,
)
QC = np.array(
    [
        [9, 9, 12, 24, 50, 50, 50, 50],
        [9, 11, 13, 33, 50, 50, 50, 50],
        [12, 13, 28, 50, 50, 50, 50, 50],
        [24, 33, 50, 50, 50, 50, 50, 50],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [50, 50, 50, 50, 50, 50, 50, 50],
    ],
    dtype=np.int32,
)


def _dct_matrix(N: int) -> np.ndarray:
    C = np.zeros((N, N), dtype=np.float64)
    for k in range(N):
        alpha = math.sqrt(1.0 / N) if k == 0 else math.sqrt(2.0 / N)
        for n in range(N):
            C[k, n] = alpha * math.cos(math.pi * (2 * n + 1) * k / (2 * N))
    return C


_DCT = _dct_matrix(BLOCK)


def dct2(block: np.ndarray) -> np.ndarray:
    return _DCT @ block @ _DCT.T


def idct2(coeff: np.ndarray) -> np.ndarray:
    return _DCT.T @ coeff @ _DCT


def pad_to_multiple(arr: np.ndarray, block: int = BLOCK):
    h, w = arr.shape
    ph = (block - (h % block)) % block
    pw = (block - (w % block)) % block
    if ph == 0 and pw == 0:
        return arr, h, w
    return np.pad(arr, ((0, ph), (0, pw)), mode="edge"), h, w


def unpad(arr: np.ndarray, h: int, w: int) -> np.ndarray:
    return arr[:h, :w]


def text_to_bits(text: str) -> str:
    data = text.encode("utf-8")
    length = len(data)
    len_bits = f"{length:032b}"
    data_bits = "".join(f"{b:08b}" for b in data)
    return len_bits + data_bits


def bits_to_text(bits: str) -> str:
    if len(bits) < 32:
        return ""
    length = int(bits[:32], 2)
    need = 32 + length * 8
    data_bits = bits[32:need]
    bytelist = [int(data_bits[i : i + 8], 2) for i in range(0, len(data_bits), 8)]
    try:
        return bytes(bytelist).decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return bytes(bytelist).decode("utf-8", errors="replace")


def capacity_in_bits(h: int, w: int) -> int:
    H = h + (BLOCK - h % BLOCK) % BLOCK
    W = w + (BLOCK - w % BLOCK) % BLOCK
    return (H // BLOCK) * (W // BLOCK)


def lsb_set_for_coeff(c: int, bit: int) -> tuple[int, int, int]:
    was_zero = c == 0
    if c == 0:
        c = 1
    mag = abs(c)
    changed_parity = 0
    if (mag & 1) != bit:
        mag += 1
        changed_parity = 1
    newc = mag if c > 0 else -mag
    return newc, was_zero, changed_parity


def lsb_get_from_coeff(c: int) -> int:
    if c == 0:
        return 0
    return abs(c) & 1


def to_zigzag_list(Q: np.ndarray) -> list:
    order = [
        (0, 0),
        (0, 1),
        (1, 0),
        (2, 0),
        (1, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (2, 1),
        (3, 0),
        (4, 0),
        (3, 1),
        (2, 2),
        (1, 3),
        (0, 4),
        (0, 5),
        (1, 4),
        (2, 3),
        (3, 2),
        (4, 1),
        (5, 0),
        (6, 0),
        (5, 1),
        (4, 2),
        (3, 3),
        (2, 4),
        (1, 5),
        (0, 6),
        (0, 7),
        (1, 6),
        (2, 5),
        (3, 4),
        (4, 3),
        (5, 2),
        (6, 1),
        (7, 0),
        (7, 1),
        (6, 2),
        (5, 3),
        (4, 4),
        (3, 5),
        (2, 6),
        (1, 7),
        (2, 7),
        (3, 6),
        (4, 5),
        (5, 4),
        (6, 3),
        (7, 2),
        (7, 3),
        (6, 4),
        (5, 5),
        (4, 6),
        (3, 7),
        (4, 7),
        (5, 6),
        (6, 5),
        (7, 4),
        (7, 5),
        (6, 6),
        (5, 7),
        (6, 7),
        (7, 6),
        (7, 7),
    ]
    return [int(Q[i, j]) for (i, j) in order]


def _bits_preview(bits: str, k: int = 32) -> str:
    if not bits:
        return ""
    if len(bits) <= 2 * k:
        return bits
    return bits[:k] + " … " + bits[-k:]


def _text_preview(s: str, k: int = 120) -> str:
    s1 = s.replace("\n", "\\n")
    return s1 if len(s1) <= k else s1[:k] + "…"


def embed_bits_into_image(img_rgb: Image.Image, bits: str) -> tuple[Image.Image, dict]:
    ycbcr = img_rgb.convert("YCbCr")
    arr = np.array(ycbcr).astype(np.float64)
    chan = arr[:, :, CHANNEL_IDX]

    chan_pad, H0, W0 = pad_to_multiple(chan, BLOCK)
    H, W = chan_pad.shape
    total_blocks = (H // BLOCK) * (W // BLOCK)

    if len(bits) > total_blocks:
        raise ValueError(
            f"Недостаточно блоков: нужно {len(bits)}, доступно {total_blocks}."
        )

    outQ = np.zeros_like(chan_pad)
    u, v = COEF_POS
    q = QY

    used_blocks = 0
    zeros_fixed = 0
    parity_changed = 0

    bit_idx = 0
    for by in range(0, H, BLOCK):
        for bx in range(0, W, BLOCK):
            block = chan_pad[by : by + BLOCK, bx : bx + BLOCK] - 128.0
            D = dct2(block)
            Cq = np.rint(D / q).astype(np.int32)

            if bit_idx < len(bits):
                b = 1 if bits[bit_idx] == "1" else 0
                target_u, target_v = (u, v) if not (u == 0 and v == 0) else (0, 1)
                newc, wz, pc = lsb_set_for_coeff(int(Cq[target_u, target_v]), b)
                Cq[target_u, target_v] = newc
                zeros_fixed += 1 if wz else 0
                parity_changed += 1 if pc else 0
                bit_idx += 1
                used_blocks += 1

            Dm = (Cq * q).astype(np.float64)
            block_rec = idct2(Dm) + 128.0
            outQ[by : by + BLOCK, bx : bx + BLOCK] = block_rec

    outY = np.clip(np.rint(outQ), 0, 255).astype(np.uint8)
    outY = unpad(outY, H0, W0)

    arr[:H0, :W0, CHANNEL_IDX] = outY
    out_ycbcr = Image.fromarray(arr[:H0, :W0].astype(np.uint8), mode="YCbCr")
    out_rgb = out_ycbcr.convert("RGB")

    stats = {
        "total_blocks": total_blocks,
        "used_blocks": used_blocks,
        "zeros_fixed": zeros_fixed,
        "parity_changed": parity_changed,
        "qy_uv": int(q[u, v]),
        "coef_pos": (u, v),
    }
    return out_rgb, stats


def extract_bits_from_image(img_rgb: Image.Image, need_bits: int) -> str:
    ycbcr = img_rgb.convert("YCbCr")
    arr = np.array(ycbcr).astype(np.float64)
    chan = arr[:, :, CHANNEL_IDX]

    chan_pad, H0, W0 = pad_to_multiple(chan, BLOCK)
    H, W = chan_pad.shape
    total_blocks = (H // BLOCK) * (W // BLOCK)
    if need_bits > total_blocks:
        raise ValueError(f"Запрошено {need_bits} бит, доступно {total_blocks}.")

    bits = []
    u, v = COEF_POS
    q = QY
    bit_idx = 0
    for by in range(0, H, BLOCK):
        for bx in range(0, W, BLOCK):
            block = chan_pad[by : by + BLOCK, bx : bx + BLOCK] - 128.0
            D = dct2(block)
            Cq = np.rint(D / q).astype(np.int32)
            c = Cq[u, v] if not (u == 0 and v == 0) else Cq[0, 1]
            bits.append("1" if lsb_get_from_coeff(int(c)) == 1 else "0")
            bit_idx += 1
            if bit_idx >= need_bits:
                break
        if bit_idx >= need_bits:
            break
    return "".join(bits)


def save_jpeg_with_qtables(img_rgb: Image.Image, path: str):
    qtables = [to_zigzag_list(QY), to_zigzag_list(QC)]
    img_rgb.save(
        path,
        format="JPEG",
        qtables=qtables,
        subsampling=0,
        quality=QUALITY,
        optimize=False,
    )


def cmd_encrypt():
    if not os.path.exists(COVER_JPG):
        raise SystemExit(
            f"Нет {COVER_JPG}. Положи исходное изображение (JPEG) рядом со скриптом."
        )
    with open(INPUT_TXT, "r", encoding="utf-8") as f:
        text = f.read()
    img = Image.open(COVER_JPG).convert("RGB")
    w, h = img.size
    cap = capacity_in_bits(h, w)
    log.info(
        "STEP 1/5 — вход: cover=%s (%dx%d px), input=%s", COVER_JPG, w, h, INPUT_TXT
    )
    log.info("         вместимость: %d бит (по 1 биту на блок 8×8)", cap)

    bits = text_to_bits(text)
    log.info(
        "STEP 2/5 — подготовка: длина текста=%d байт, будет записано %d бит (с длиной).",
        len(text.encode("utf-8")),
        len(bits),
    )
    if len(bits) > cap:
        raise SystemExit(
            f"Сообщение слишком длинное: нужно {len(bits)} бит, доступно {cap}."
        )
    log.info(
        "         канал=Y, coef=(%d,%d), QY=%d",
        COEF_POS[0],
        COEF_POS[1],
        int(QY[COEF_POS]),
    )
    log.info(
        "         preview(bits): %s | %s",
        _bits_preview(bits),
        _bits_preview(bits[-64:]),
    )

    stego_rgb, stats = embed_bits_into_image(img, bits)
    log.info(
        "         встраивание: использовано блоков=%d из %d (%.2f%%), оживлено нулей=%d, смена чётности=%d",
        stats["used_blocks"],
        stats["total_blocks"],
        100.0 * stats["used_blocks"] / stats["total_blocks"],
        stats["zeros_fixed"],
        stats["parity_changed"],
    )

    save_jpeg_with_qtables(stego_rgb, STEGO_JPG)
    log.info(
        "STEP 3/5 — сохранение: %s (qtables=IJG~%d, subsampling=4:4:4)",
        STEGO_JPG,
        QUALITY,
    )

    stego_check = Image.open(STEGO_JPG).convert("RGB")
    length_bits = extract_bits_from_image(stego_check, 32)
    msg_len = int(length_bits, 2)
    total_needed = 32 + msg_len * 8
    log.info(
        "STEP 4/5 — самопроверка: длина=%d байт → всего %d бит", msg_len, total_needed
    )
    bits_back = extract_bits_from_image(stego_check, total_needed)
    txt_back = bits_to_text(bits_back)
    ok = txt_back == text
    log.info(
        "         bits(check) : %s | %s",
        _bits_preview(bits_back),
        _bits_preview(bits_back[-64:]),
    )
    log.info('         text preview: "%s"', _text_preview(txt_back))
    log.info("         результат    : %s", "OK" if ok else "MISMATCH")

    log.info("STEP 5/5 — готово.")
    print(f"OK: {INPUT_TXT} -> {STEGO_JPG}")


def cmd_decrypt():
    if not os.path.exists(STEGO_JPG):
        raise SystemExit(f"Нет {STEGO_JPG}. Сначала запусти encrypt.")
    img = Image.open(STEGO_JPG).convert("RGB")
    w, h = img.size
    log.info("STEP 1/3 — вход: stego=%s (%dx%d px)", STEGO_JPG, w, h)

    len_bits = extract_bits_from_image(img, 32)
    msg_len = int(len_bits, 2)
    total_bits = 32 + msg_len * 8
    log.info(
        "STEP 2/3 — извлечение: длина=%d байт (len_bits=%s), всего %d бит",
        msg_len,
        _bits_preview(len_bits),
        total_bits,
    )

    bits = extract_bits_from_image(img, total_bits)
    text = bits_to_text(bits)
    log.info(
        "         bits preview : %s | %s",
        _bits_preview(bits),
        _bits_preview(bits[-64:]),
    )
    log.info('         text preview : "%s"', _text_preview(text))

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write(text)
    log.info("STEP 3/3 — записано в %s", OUTPUT_TXT)
    print(f"OK: {STEGO_JPG} -> {OUTPUT_TXT}")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("encrypt", "decrypt"):
        print("Использование:")
        print("  python main.py encrypt   прочитать input.txt + cover.jpg -> stego.jpg")
        print("  python main.py decrypt   прочитать stego.jpg -> output.txt")
        raise SystemExit(1)
    cmd = sys.argv[1]
    if cmd == "encrypt":
        cmd_encrypt()
    elif cmd == "decrypt":
        cmd_decrypt()


if __name__ == "__main__":
    main()
