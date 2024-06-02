import math
import random


from ot_additional import get_prime_number, euclidian_extended, chinese_algorithm


def get_e(base: int) -> int:
    e = random.randrange(2, base - 1)
    while math.gcd(e, base) != 1:
        e = random.randrange(2, base - 1)
    return e


def get_d(e: int, base: int) -> int:
    # result = egcd(e, base)[1]
    # if result < 0:
    #     result += base
    # return result
    return euclidian_extended(e, base)


def keygen() -> list[tuple]:
    # bit_size = int(input("Введите размер в битах для 2 больших простых чисел: "))
    bit_size = 128
    q = get_prime_number(bit_size)
    p = get_prime_number(bit_size)
    n = p * q
    fi_n = (p - 1) * (q - 1)
    e = get_e(fi_n)
    d = get_d(e, fi_n)
    return [(p, q, d), (n, e)]


def encryption(open_key: tuple, text: int) -> int:
    return pow(text, open_key[1], open_key[0])


def decryption(secret_key: tuple, cipher_text: int) -> int:
    return chinese_algorithm(secret_key[0], secret_key[1], cipher_text, secret_key[2])
