def decode_entry(entry):
    digits = {
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
    result = ''
    for i in range(0, 27, 3):
        segment = ''.join([line[i:i+3] for line in entry[:3]])
        result += digits.get(segment, '?')
    return result.strip()


def validate_account_number(account_number):
    if len(account_number) != 9 or not account_number.isdigit():
        return False
    total = sum((i + 1) * int(digit) for i, digit in enumerate(account_number))
    return total % 11 == 0


def classify_entry(account_number):
    if '?' in account_number:
        return account_number + ' ILL'
    if not validate_account_number(account_number):
        return account_number + ' ERR'
    return account_number


def repair_entry(account_number):
    if account_number.count('?') > 1:
        return account_number + ' ILL'
    possible_numbers = []
    for i in range(9):
        if account_number[i] == '?':
            for digit in '0123456789':
                candidate = account_number[:i] + digit + account_number[i + 1:]
                if validate_account_number(candidate):
                    possible_numbers.append(candidate)
    if len(possible_numbers) == 0:
        return account_number + ' ERR'
    if len(possible_numbers) == 1:
        return possible_numbers[0]
    return account_number + ' AMB ' + str(possible_numbers)