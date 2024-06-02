import random

from additional import generate_base_key, generate_protocol_variables
from ot import start_ot
from aes import key_expansion, decrypt

output_strings = ["====Таблица истинности ", "====Зашифрованные выходные значения ", "===="]


DECRYPT_PLAN = {
    'and_1': ['b', 'c'],
    'xor_1': ['a', 'b'],
    'not_1': ['c', 'c'],
    'and_2': ['xor_1', 'not_1'],
    'and_3': ['and_2', 'd'],
    'final': ['and_1', 'and_3']
}


def generate_base_keys_list() -> dict[str: list[str]]:
    base_keys = dict()
    inputs = ['a', 'b', 'c', 'd']
    for i in range(4):
        base_keys_row = []
        for j in range(2):
            base_keys_row.append(generate_base_key())
        base_keys[inputs[i]] = base_keys_row
    # for i in inputs:
    #     print(base_keys.get(i))
    return base_keys


def generate_intermediate_keys(truth_table: list[list], gate_name: str) -> list:
    if "not" not in gate_name:
        tempt_result_row = [truth_table[0][2]]
        for i in truth_table:
            if i[2] not in tempt_result_row:
                tempt_result_row.append(i[2])
        result_row = []
        for i in tempt_result_row:
            string_version = ""
            for j in range(len(i) // 2):
                string_version += i[j]
            result_row.append(string_version)
        return result_row
    else:
        tempt_result_row = [truth_table[0][1]]
        for i in truth_table:
            if i[1] not in tempt_result_row:
                tempt_result_row.append(i[1])
        result_row = []
        for i in tempt_result_row:
            string_version = ""
            for j in range(len(i) // 2):
                string_version += i[j]
            result_row.append(string_version)
        return result_row


def print_gate_data(gate: tuple, truth_table_name: str):
    count = 0
    for i in gate:
        print(output_strings[count] + truth_table_name + output_strings[-1])
        for j in i:
            print(j)
        count += 1


def encrypt_scheme() -> tuple[dict, dict, dict]:
    base_keys = generate_base_keys_list()
    intermediate_keys = dict()
    gates = dict()
    gates['and_1'] = generate_protocol_variables("AND", [base_keys.get('b'), base_keys.get('c')], "and_1")
    gates['xor_1'] = generate_protocol_variables("XOR", [base_keys.get('a'), base_keys.get('b')], "and_1")
    gates['not_1'] = generate_protocol_variables("NOT", [base_keys.get('c')], "not_1")
    for gate in gates:
        # print_gate_data(gates.get(gate), gate)
        intermediate_keys[gate] = (generate_intermediate_keys(gates.get(gate)[0], gate))
    # print("====Промежуточные ключи====")
    # for i in intermediate_keys:
    #     print(f'{i}: {intermediate_keys.get(i)}')
    gates['and_2'] = generate_protocol_variables("AND",
                                                 [intermediate_keys.get('xor_1'), intermediate_keys.get('not_1')],
                                                 "and_2")
    # print_gate_data(gates.get('and_2'), 'and_2')
    intermediate_keys['and_2'] = (generate_intermediate_keys(gates.get('and_2')[0], 'and_2'))
    # print("====Промежуточные ключи====")
    # for i in intermediate_keys:
    #     print(f'{i}: {intermediate_keys.get(i)}')
    gates['and_3'] = generate_protocol_variables("AND", [intermediate_keys.get('and_2'), base_keys.get('d')], "and_3")
    # print_gate_data(gates.get('and_3'), 'and_3')
    intermediate_keys['and_3'] = (generate_intermediate_keys(gates.get('and_3')[0], 'and_3'))
    # print("====Промежуточные ключи====")
    # for i in intermediate_keys:
    #     print(f'{i}: {intermediate_keys.get(i)}')
    gates['final'] = generate_protocol_variables("AND",
                                                 [intermediate_keys.get('and_1'), intermediate_keys.get('and_3')],
                                                 "final")
    # print_gate_data(gates.get('final'), 'final')
    intermediate_keys['final'] = (generate_intermediate_keys(gates.get('final')[0], 'final'))
    # print("====Промежуточные ключи====")
    # for i in intermediate_keys:
    #     print(f'{i}: {intermediate_keys.get(i)}')
    encrypted_gates = dict()
    for i in gates:
        encrypted_gates[i] = gates.get(i)[1]
    return base_keys, intermediate_keys, encrypted_gates


def encryptor_output(base_keys: dict, intermediate_keys: dict, encrypted_gates: dict):
    print("====Базовые ключи====")
    for i in base_keys:
        print(f'\t{i}: {base_keys.get(i)}')
    print("===Промежуточные ключи====")
    for i in intermediate_keys:
        print(f'\t{i}: {intermediate_keys.get(i)}')
    print("====Зашифрованные выходы каждого гейта====")
    for i in encrypted_gates:
        print(f'\t====gate: {i}====')
        for j in encrypted_gates.get(i):
            print(f'\t{j}')


def data_for_decrypt(alice_keys: list[str], bob_keys: list[str], base_key: dict, encrypted_gates: dict) -> dict:
    print("Укажите какие ключи Алиса хочет отправить Бобу")
    key_pair = dict()
    keys = []
    for i in range(2):
        # keys.append(int(input(f'\t{i + 1} ключ: ')))
        keys.append(random.randint(0, 1))
        key_pair[alice_keys[i]] = base_key.get(alice_keys[i])[keys[-1]]
    print("====Алиса отправлет Бобу следующие ключи====")
    for i in key_pair:
        print(f'\tA -> B: [{i}:{key_pair.get(i)}]')
    print("===Алиса отправлет Бобу зашифрованные выходы гейтов=====")
    for i in encrypted_gates:
        print(f'\t====gate: {i}====')
        for j in encrypted_gates.get(i):
            print(f'\t{j}')
    print("Укажите какие ключи Боб хочет получить от Алисы")
    needed_keys = []
    print("====Передача ключей, используя OT====")
    for i in range(2):
        # needed_keys.append(int(input(f'\t{i + 1} ключ: ')))
        needed_keys.append(random.randint(0, 1))
        key_pair[bob_keys[i]] = start_ot(base_key.get(bob_keys[i]), needed_keys[i])
        print(f'\tA -> B (OT): [{bob_keys[i]}: {key_pair.get(bob_keys[i])}]')
    return key_pair


def decrypt_gate(all_keys: list, gate_entry: list) -> str:
    for entry in gate_entry:
        temp_value = decrypt(entry, all_keys)
        decrypt_value = ''
        for i in temp_value:
            decrypt_value += i.lower()
        if decrypt_value[16:] == "0000000000000000":
            return decrypt_value[:16]
    return f'Ошибка при дешифровании'


def decrypt_step(gate_name: str, chosen_keys: dict, intermediate_keys: dict, gate_keys: list[str], encrypted_gates: dict) -> str:
    print(f"====Расшифровка gate {gate_name}====")
    result = ''
    if gate_keys[0] in chosen_keys and gate_keys[1] in chosen_keys:
        all_keys = key_expansion(chosen_keys.get(gate_keys[0]) + chosen_keys.get(gate_keys[1]))
    elif gate_keys[0] in intermediate_keys and gate_keys[1] in chosen_keys:
        all_keys = key_expansion(intermediate_keys.get(gate_keys[0]) + chosen_keys.get(gate_keys[1]))
    elif gate_keys[0] in chosen_keys and gate_keys[1] in intermediate_keys:
        all_keys = key_expansion(chosen_keys.get(gate_keys[0]) + intermediate_keys.get(gate_keys[1]))
    else:
        all_keys = key_expansion(intermediate_keys.get(gate_keys[0]) + intermediate_keys.get(gate_keys[1]))
    result = decrypt_gate(all_keys, encrypted_gates.get(gate_name))
    print(f'B: [{gate_name}: {result}]')
    return result


def decrypt_scheme(chosen_keys: dict, encrypted_gates: dict) -> str:
    intermediate_keys = dict()
    for step in DECRYPT_PLAN:
        intermediate_keys[step] = decrypt_step(step, chosen_keys, intermediate_keys, DECRYPT_PLAN.get(step), encrypted_gates)
    return intermediate_keys.get('final')


'''
    1. Алиса(шифровальщик) полность шифрует контур (✔️)
    2. Алиса отправляет зашифрованные выходы каждого гейта и 2 своих ключа (✔️) 
    3. Боб(вычислитель) получает 2 своих ключа от Алисы используя OT (✔️)
    4. Боб производит расшифрование контура и отправляет результат Алисе (✔️)
    5. Максим в муте (❌)
'''


def main():
    base_keys, intermediate_keys, encrypted_gates = encrypt_scheme()
    encryptor_output(base_keys, intermediate_keys, encrypted_gates)
    print()
    chosen_keys = data_for_decrypt(['a', 'c'], ['b', 'd'], base_keys, encrypted_gates)
    # for i in chosen_keys:
    #     print(f'{i}: {chosen_keys.get(i)}')
    print("====Боб начинает расшифровку контура====")
    result = decrypt_scheme(chosen_keys, encrypted_gates)
    print()
    print(f'B -> A: {result}')

if __name__ == "__main__":
    main()
