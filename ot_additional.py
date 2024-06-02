import math
import random


def get_prime_number(bit_size: int) -> int:
    flag = False
    while not flag:
        prime_number = random.randrange(int(math.pow(2, bit_size - 1)), int(math.pow(2, bit_size) - 1))
        if prime_number % 2 == 0:
            prime_number += 1
        flag = True
        for i in range(1, 50):
            a = random.randrange(2, prime_number - 2)
            if pow(a, prime_number - 1, prime_number) % prime_number != 1:
                flag = False
                break
        if flag:
            return prime_number
        else:
            continue


def euclidian_extended(a: int, b: int) -> int:
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx * q
        y, yy = yy, y - yy * q
    return x


def casting(x: int, exponent: int, modulo: int) -> int:
    return pow(x % modulo, exponent % (modulo - 1), modulo)


def chinese_algorithm(p: int, q: int, x: int, x_exponent: int) -> int:
    moduls = [p, q]
    equations = []
    for i in range(len(moduls)):
        equations.append((casting(x, x_exponent, moduls[i]), moduls[i]))
    # print(equations)
    modulo = p * q
    results = []
    for i in range(len(equations)):
        results.append((equations[i][0], modulo // equations[i][1],
                        euclidian_extended(modulo // equations[i][1], equations[i][1])))
    return (results[0][0] * results[0][1] * results[0][2] + results[1][0] * results[1][1] * results[1][2]) % modulo

