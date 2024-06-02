from aes import encrypt, key_expansion
from random import randint


LOGICAL_AND_TRUTH_TABLE = (
    (0, 0, 0),
    (0, 1, 0),
    (1, 0, 0),
    (1, 1, 1)
)

LOGICAL_XOR_TRUTH_TABLE = (
    (0, 0, 0),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 0)
)


def generate_key_for_encrypt() -> list:
    key = []
    for t in range(8):
        key.append(hex(randint(0, 255))[2:])
        if len(key[t]) < 2:
            key[t] = '0' + key[t]
    for t in range(8):
        key.append('00')
    return key


def generate_base_key() -> str:
    size = 8
    key = ''
    for t in range(size):
        temp = hex(randint(0, 255))[2:]
        if len(temp) < 2:
            temp = '0' + temp
        key += temp
    return key


def generate_keys(chosen_truth_table: str, base_keys: list[list], gate_name: str) -> list[dict[str:list]]:
    if chosen_truth_table != "NOT":
        key_table = []
        for i in range(2):
            key_row = dict()
            for j in range(2):
                key_row[f'k_{i}_{j}'] = base_keys[i][j]
            key_table.append(key_row)
        key_row = dict()
        if "final" not in gate_name:
            for j in range(2):
                key_row[f'k_2_{j}'] = generate_key_for_encrypt()
        else:
            key_row[f'k_2_0'] = ['00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00',
                                 '00', '00']
            key_row[f'k_2_1'] = ['11', '11', '11', '11', '11', '11', '11', '11', '00', '00', '00', '00', '00', '00',
                                 '00', '00']
        key_table.append(key_row)
        # print("====Создание таблицы ключей====")
        # for i in key_table:
        #     print(i)
        return key_table
    else:
        key_table = []
        for i in range(2):
            key_row = {f'k_{i}_0': base_keys[0][i]}
            key_table.append(key_row)
            key_table[i].update({f'k_{i}_1': generate_key_for_encrypt()})
        # print("====Создание таблицы ключей====")
        # for i in key_table:
        #     print(i)
        return key_table


def create_truth_table(key_table: list[dict], chosen_truth_table: str) -> list[list]:
    logical_truth_table = ''
    match chosen_truth_table:
        case 'AND': logical_truth_table = LOGICAL_AND_TRUTH_TABLE
        case 'XOR': logical_truth_table = LOGICAL_XOR_TRUTH_TABLE
    if chosen_truth_table != "NOT":
        truth_table = []
        for i in logical_truth_table:
            table_row = []
            row_count = 0
            for j in i:
                if j == 0:
                    table_row.append(key_table[row_count].get(f'k_{row_count}_{0}'))
                else:
                    table_row.append(key_table[row_count].get(f'k_{row_count}_{1}'))
                row_count += 1
            truth_table.append(table_row)
        # print(f"====Создание таблицы истинности для {chosen_truth_table}, ассоциированной с ключами====")
        # for i in truth_table:
        #     print(i)
        return truth_table
    else:
        truth_table = []
        for i in range(2):
            row_number = abs(i - 1)
            table_row = [key_table[i].get(f'k_{i}_0'), key_table[row_number].get(f'k_{row_number}_1')]
            truth_table.append(table_row)
        # print(f"====Создание таблицы истинности для {chosen_truth_table}, ассоциированной с ключами====")
        # for i in truth_table:
        #     print(i)
        return truth_table


def create_encrypted_output(truth_table: list[list], chosen_truth_table: str) -> list[list]:
    if chosen_truth_table != "NOT":
        temp_truth_table = []
        for i in range(len(truth_table)):
            all_keys = key_expansion(truth_table[i][0] + truth_table[i][1])
            temp_truth_table.append(encrypt(truth_table[i][2], all_keys))
        # print(f"====Чистые зашифрованные выходные значения {chosen_truth_table} gate====")
        # for i in temp_truth_table:
        #     print(i)
        final_truth_table = ['', '', '', '']
        indexes = []
        for i in range(len(final_truth_table)):
            index = randint(0, len(final_truth_table) - 1)
            while index in indexes:
                index = randint(0, len(final_truth_table) - 1)
            final_truth_table[index] = temp_truth_table[i]
            indexes.append(index)
        # print(f"====Перемешанные зашифрованные выходные значения {chosen_truth_table} gate====")
        # for i in final_truth_table:
        #     print(i)
        return final_truth_table
    else:
        temp_truth_table = []
        for i in range(len(truth_table)):
            all_keys = key_expansion(truth_table[i][0] * 2)
            temp_truth_table.append(encrypt(truth_table[i][1] * 2, all_keys))
        # print(f"====Чистые зашифрованные выходные значения {chosen_truth_table} gate====")
        # for i in temp_truth_table:
        #     print(i)
        final_truth_table = ['', '']
        indexes = []
        for i in range(len(final_truth_table)):
            index = randint(0, len(final_truth_table) - 1)
            while index in indexes:
                index = randint(0, len(final_truth_table) - 1)
            final_truth_table[index] = temp_truth_table[i]
            indexes.append(index)
        # print(f"====Перемешанные зашифрованные выходные значения {chosen_truth_table} gate====")
        # for i in final_truth_table:
        #     print(i)
        return final_truth_table


def generate_protocol_variables(logical_func: str, base_keys: list[list], gate_name: str) -> tuple:
    key_table = generate_keys(logical_func, base_keys, gate_name)
    truth_table = create_truth_table(key_table, logical_func)
    final_truth_table = create_encrypted_output(truth_table, logical_func)
    return truth_table, final_truth_table


# generate_protocol_variables("XOR")
