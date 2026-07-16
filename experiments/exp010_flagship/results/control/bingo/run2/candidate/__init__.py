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
    elif 61 <= number <= 75:
        return 'O'

def create_card(numbers):
    validate_card(numbers)
    card = [[numbers[i] for i in range(j, len(numbers), 5)] for j in range(5)]
    card[2][2] = None  # Center space is free
    return card

def validate_card(numbers):
    if len(set(numbers)) != 24:
        raise ValueError('card numbers must be unique')
    if len(numbers) != 24:
        raise ValueError('exactly 24 numbers are required')
    for number in numbers:
        if number < 1 or number > 75:
            if number in range(1, 16):
                raise ValueError('number not valid for column B')
            elif number in range(16, 31):
                raise ValueError('number not valid for column I')
            elif number in range(31, 46):
                raise ValueError('number not valid for column N')
            elif number in range(46, 61):
                raise ValueError('number not valid for column G')
            elif number in range(61, 76):
                raise ValueError('number not valid for column O')

def mark_number(card, number):
    if number < 1 or number > 75:
        raise ValueError('number must be between 1 and 75')
    marked = [[False] * 5 for _ in range(5)]
    hit = False
    for i in range(5):
        for j in range(5):
            if card[i][j] == number:
                marked[i][j] = True
                hit = True
    return marked, hit

def check_win(card, marked):
    # Check rows
    for row in marked:
        if all(row):
            return True
    # Check columns
    for j in range(5):
        if all(marked[i][j] for i in range(5)):
            return True
    # Check diagonals
    if all(marked[i][i] for i in range(5)):
        return True
    if all(marked[i][4 - i] for i in range(5)):
        return True
    return False