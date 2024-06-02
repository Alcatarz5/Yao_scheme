import math

from rsa import keygen
from random import randint


def get_secrets() -> tuple:
    input_string = input("Введите 2 секрета через пробел: \n").split(' ')
    return int(input_string[0]), int(input_string[1])


def get_two_random_number(modulo: int) -> tuple:
    first_number = randint(2, modulo - 1)
    while math.gcd(first_number, modulo) != 1:
        first_number = randint(2, modulo - 1)
    second_number = randint(2, modulo - 1)
    while math.gcd(second_number, modulo) != 1 and second_number != first_number:
        second_number = randint(2, modulo - 1)
    return first_number, second_number


def start_ot(secrets: list, chosen_key: int):
    # a_0, a_1 = get_secrets()
    a_0 = int(secrets[0], 16)
    a_1 = int(secrets[1], 16)
    secret_key, open_key = keygen()
    r_0, r_1 = get_two_random_number(open_key[0])

    chosen_rand = 0
    if chosen_key == 0:
        chosen_rand = r_0
    else:
        chosen_rand = r_1
    k = randint(2, open_key[0] - 1)
    x = (chosen_rand + pow(k, open_key[1], open_key[0])) % open_key[0]

    y_0 = (a_0 + pow((x - r_0) % open_key[0], secret_key[2], open_key[0])) % open_key[0]
    y_1 = (a_1 + pow((x - r_1) % open_key[0], secret_key[2], open_key[0])) % open_key[0]

    answer = 0
    if chosen_key == 0:
        answer = hex((y_0 - k) % open_key[0])[2:]
        if len(answer) < 16:
            answer = '0' + answer
    else:
        answer = hex((y_1 - k) % open_key[0])[2:]
        if len(answer) < 16:
            answer = '0' + answer

    return answer


# print(start_ot(['f24181d67199be10', '35d4d68ecbe57c28'], 1))