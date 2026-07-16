def announce_column(number):
    if number < 1 or number > 75:
        raise ValueError('number must be between 1 and 75')
    if 1 <= number <= 15:
        return 'B'
    elif 16 <= number <= 30:
        return 'I'
    elif 31 <= number <= 45:
        return 'N'
    elif 46 <= number <= 60:
        return 'G'
    else:
        return 'O'

def lay_out_card(numbers):
    if len(numbers) != 24:
        raise ValueError('exactly 24 numbers are required')
    if len(set(numbers)) != len(numbers):
        raise ValueError('card numbers must be unique')
    validate_card(numbers)
    card = [[None] * 5 for _ in range(5)]
    card[0] = sorted(n for n in numbers if 1 <= n <= 15)  # B column
    card[1] = sorted(n for n in numbers if 16 <= n <= 30)  # I column
    card[2] = [numbers[10], numbers[11], None, numbers[12], numbers[13]]  # N column with free space
    card[3] = sorted(n for n in numbers if 46 <= n <= 60)  # G column
    card[4] = sorted(n for n in numbers if 61 <= n <= 75) + [75]  # Ensure O column has 5 values
    return card

def validate_card(numbers):
    if len(set(numbers)) != len(numbers):
        raise ValueError('card numbers must be unique')
    if any(not (1 <= n <= 15) for n in numbers[0:5]):
        raise ValueError(f'B column has an invalid number {next(n for n in numbers[0:5] if not (1 <= n <= 15))}')
    if any(not (16 <= n <= 30) for n in numbers[5:10]):
        raise ValueError(f'I column has an invalid number {next(n for n in numbers[5:10] if not (16 <= n <= 30))}')
    if any(not (31 <= n <= 45) for n in numbers[10:15]):
        raise ValueError(f'N column has an invalid number {next(n for n in numbers[10:15] if not (31 <= n <= 45))}')
    if any(not (46 <= n <= 60) for n in numbers[15:20]):
        raise ValueError(f'G column has an invalid number {next(n for n in numbers[15:20] if not (46 <= n <= 60))}')
    if any(not (61 <= n <= 75) for n in numbers[20:]):
        raise ValueError(f'O column has an invalid number {next(n for n in numbers[20:] if not (61 <= n <= 75))}')


def mark_called_number(card, number):
    if number < 1 or number > 75:
        raise ValueError('number must be between 1 and 75')
    hit = False
    for i in range(5):
        for j in range(5):
            if card[i][j] == number:
                card[i][j] = 'X'
                hit = True
    return card, hit


def detect_win(card):
    for row in card:
        if all(x == 'X' for x in row):
            return True
    for col in range(5):
        if all(card[row][col] == 'X' for row in range(5)):
            return True
    if all(card[i][i] == 'X' for i in range(5)):
        return True
    if all(card[i][4 - i] == 'X' for i in range(5)):
        return True
    return False
