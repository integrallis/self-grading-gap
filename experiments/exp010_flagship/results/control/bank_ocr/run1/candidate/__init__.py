def decode_entry(input_data):
    if len(input_data) != 3:
        raise ValueError('entry must have exactly three lines')

    digits = ''
    for i in range(0, 27, 3):  # 9 digits, 3 columns each
        digit = input_data[1][i:i + 3] + input_data[2][i:i + 3]
        digits += decode_digit(digit)

    return digits


def decode_digit(digit):
    patterns = {
        ' _ | ||_|': '0',
        '     |  |': '1',
        ' _  _||_ ': '2',
        ' _  _| _|': '3',
        '   |_|  |': '4',
        ' _ |_  _|': '5',
        ' _ |_||_|': '6',
        ' _   |  |': '7',
        ' _ |_||_|': '8',
        ' _ |_| _|': '9'
    }
    return patterns.get(digit, '?')


def validate_checksum(account_number):
    if len(account_number) != 9 or not account_number.isdigit():
        return False
    total = sum(int(digit) * (9 - i) for i, digit in enumerate(account_number))
    return total % 11 == 0


def classify_entry(account_number):
    if '?' in account_number:
        return f'{account_number} ILL'
    if not validate_checksum(account_number):
        return f'{account_number} ERR'
    return account_number


def repair_entry(account_number):
    if '?' in account_number:
        return f'{account_number} ILL'

    possible_repair = []
    for i in range(9):
        for replacement in '0123456789':
            candidate = account_number[:i] + replacement + account_number[i + 1:]
            if validate_checksum(candidate):
                possible_repair.append(candidate)

    if len(possible_repair) == 0:
        return f'{account_number} ERR'
    if len(possible_repair) == 1:
        return possible_repair[0]
    return f'{account_number} AMB {possible_repair}'
