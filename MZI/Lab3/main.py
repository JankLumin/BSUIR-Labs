import random
from typing import Tuple, List


class RabinCryptosystem:
    def __init__(self, bit_length: int = 512):
        self.bit_length = bit_length
        self.p, self.q, self.n = self._generate_keys()

    def _is_prime(self, n: int, k: int = 20) -> bool:
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False
        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def _generate_prime(self) -> int:
        while True:
            p = random.getrandbits(self.bit_length)
            p |= (1 << (self.bit_length - 1)) | 1
            p = (p // 4) * 4 + 3
            if self._is_prime(p):
                return p

    def _generate_keys(self) -> Tuple[int, int, int]:
        p = self._generate_prime()
        q = self._generate_prime()
        while p == q:
            q = self._generate_prime()
        n = p * q
        print(f"   p = {p}")
        print(f"   q = {q}")
        print(f"   n = {n}")
        print(f"   Размер ключа: {n.bit_length()} бит")
        return p, q, n

    def _extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self._extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def _crt(self, a1: int, a2: int) -> int:
        _, x, y = self._extended_gcd(self.p, self.q)
        return (a1 * self.q * y + a2 * self.p * x) % self.n

    def encrypt(self, message: int) -> int:
        if message >= self.n:
            raise ValueError("Сообщение должно быть меньше n")
        return pow(message, 2, self.n)

    def decrypt(self, ciphertext: int) -> List[int]:
        mp = pow(ciphertext, (self.p + 1) // 4, self.p)
        mq = pow(ciphertext, (self.q + 1) // 4, self.q)
        solutions = [
            self._crt(mp, mq),
            self._crt(mp, self.q - mq),
            self._crt(self.p - mp, mq),
            self._crt(self.p - mp, self.q - mq),
        ]
        return solutions

    def encrypt_bytes(self, data: bytes) -> bytes:
        message_int = int.from_bytes(data, "big")
        if message_int >= self.n:
            raise ValueError("Данные слишком велики для шифрования")
        cipher_int = self.encrypt(message_int)
        cipher_bytes = cipher_int.to_bytes((cipher_int.bit_length() + 7) // 8, "big")
        return cipher_bytes

    def decrypt_bytes(self, cipher_data: bytes) -> List[bytes]:
        cipher_int = int.from_bytes(cipher_data, "big")
        solutions = self.decrypt(cipher_int)
        result = []
        for solution in solutions:
            try:
                byte_length = (solution.bit_length() + 7) // 8
                if byte_length > 0:
                    decrypted_bytes = solution.to_bytes(byte_length, "big")
                    result.append(decrypted_bytes)
            except:
                continue
        return result


def rabin_encrypt_file(input_file: str, output_file: str, rabin: RabinCryptosystem):
    with open(input_file, "rb") as f:
        plaintext = f.read()
    print(f"   Размер исходных данных: {len(plaintext)} байт")
    print(f"   Максимальный размер блока: {(rabin.n.bit_length() - 1) // 8} байт")
    max_block_size = (rabin.n.bit_length() - 1) // 8
    if len(plaintext) > max_block_size:
        raise ValueError(f"Файл слишком большой. Максимум: {max_block_size} байт")
    ciphertext = rabin.encrypt_bytes(plaintext)
    with open(output_file, "wb") as f:
        f.write(ciphertext)
    print(f"Файл зашифрован в '{output_file}'")
    print(f"Размер зашифрованного файла: {len(ciphertext)} байт")


def rabin_decrypt_file(input_file: str, output_file: str, rabin: RabinCryptosystem):
    with open(input_file, "rb") as f:
        ciphertext = f.read()
    print(f"Размер зашифрованных данных: {len(ciphertext)} байт")
    possible_results = rabin.decrypt_bytes(ciphertext)
    print(f"Найдено {len(possible_results)} возможных решений")
    for i, data in enumerate(possible_results):
        try:
            decoded = data.decode("utf-8", errors="replace")
            print()
            print(f"   Вариант {i+1}: {decoded[:100]}... ({len(data)} байт)")
        except:
            print()
            print(f"   Вариант {i+1}: [бинарные данные] ({len(data)} байт)")

    correct_data = None
    for i, data in enumerate(possible_results):
        try:
            decoded = data.decode("utf-8")
            if decoded.isprintable() or len(decoded) > 0:
                correct_data = data
                print()
                print(f"   Выбран вариант {i+1} как корректный")
                break
        except:
            continue
    if correct_data is None and possible_results:
        correct_data = possible_results[0]
        print()
        print(f"   Используем первый вариант")
    if correct_data is None:
        raise ValueError("Не удалось дешифровать данные")
    with open(output_file, "wb") as f:
        f.write(correct_data)
    print(f"Файл расшифрован в '{output_file}'")


def save_keys(rabin: RabinCryptosystem, filename: str):
    with open(filename, "w") as f:
        f.write(f"p={rabin.p}\n")
        f.write(f"q={rabin.q}\n")
        f.write(f"n={rabin.n}\n")
    print(f"Ключи занесены в '{filename}'")


def load_keys(filename: str) -> Tuple[int, int, int]:
    with open(filename, "r") as f:
        lines = f.readlines()
    p = int(lines[0].split("=")[1])
    q = int(lines[1].split("=")[1])
    n = int(lines[2].split("=")[1])
    print(f"Ключи загружены из '{filename}'")
    return p, q, n


if __name__ == "__main__":
    rabin = RabinCryptosystem(bit_length=512)
    save_keys(rabin, "rabin_keys.txt")
    test_text = "testmessage тестовоесообщение !№;%:?*()"
    with open("test_rabin.txt", "w", encoding="utf-8") as f:
        f.write(test_text)
    print(f"\nСоздан тестовый файл: {len(test_text)} символов")
    print(f"Исходный текст: {test_text}")
    try:
        rabin_encrypt_file("test_rabin.txt", "encrypted_rabin.bin", rabin)
    except ValueError as e:
        print(f"Ошибка: {e}")
        max_size = (rabin.n.bit_length() - 1) // 8
        test_text = test_text[:max_size]
        with open("test_rabin_small.txt", "w", encoding="utf-8") as f:
            f.write(test_text)
        rabin_encrypt_file("test_rabin_small.txt", "encrypted_rabin.bin", rabin)
    rabin_decrypt_file("encrypted_rabin.bin", "decrypted_rabin.txt", rabin)
    with open("decrypted_rabin.txt", "r", encoding="utf-8") as f:
        decrypted_text = f.read()
    print(f"   Исходный текст: '{test_text}'")
    print(f"   Расшифрованный текст: '{decrypted_text}'")
