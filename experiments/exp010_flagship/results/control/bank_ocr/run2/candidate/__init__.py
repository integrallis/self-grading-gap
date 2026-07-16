import pytest

def decode_entry(input_data):
    if len(input_data) != 3 or any(len(line) != 27 for line in input_data):
        raise ValueError('entry must have exactly three lines')

    digits = []
    for i in range(9):
        digit = (input_data[0][i * 3:i * 3 + 3], input_data[1][i * 2:i * 2 + 2], input_data[2][i * 3:i * 3 + 3])
        digits.append(decode_digit(digit))
    return ''.join(digits)

def decode_digit(digit):
    patterns = {
        ' _ | ||_|': '0',
        '     |  |': '1',
        ' _  _||_ ': '2',
        ' _  _| _|': '3',
        '   |_|  |': '4',
        ' _ |_  _|': '5',
        ' _ |_ |_|': '6',
        ' _   |  |': '7',
        ' _ |_||_|': '8',
        ' _ |_| _|': '9',
    }
    joined = ''.join(digit)
    return patterns.get(joined, '?')


def validate_account_number(account_number):
    if len(account_number) != 9 or not account_number.isdigit():
        return False

    total = sum(int(digit) * (9 - i) for i, digit in enumerate(account_number))
    return total % 11 == 0


def classify_entry(account_number):
    if '?' in account_number:
        return account_number + ' ILL'
    elif not validate_account_number(account_number):
        return account_number + ' ERR'
    return account_number


def repair_entry(account_number):
    if not validate_account_number(account_number) and '?' not in account_number:
        return account_number + ' ERR'
    if '?' in account_number:
        possible_numbers = generate_possible_numbers(account_number)
        if not possible_numbers:
            return account_number + ' ILL'
        if len(possible_numbers) == 1:
            return possible_numbers[0]
        return f'{possible_numbers[0]} AMB {possible_numbers}'
    return account_number


def generate_possible_numbers(account_number):
    possible_numbers = []
    for i in range(len(account_number)):
        if account_number[i] == '?':
            for digit in range(10):
                candidate = account_number[:i] + str(digit) + account_number[i+1:]
                if validate_account_number(candidate):
                    possible_numbers.append(candidate)
    return possible_numbers