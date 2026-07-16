def announce_column(number):
    if number < 1 or number > 75:
        raise ValueError("number must be between 1 and 75")
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

def create_card(numbers):
    if len(numbers) != 24:
        raise ValueError("exactly 24 numbers are required")
    if len(set(numbers)) != 24:
        raise ValueError("card numbers must be unique")

    column_ranges = {
        'B': range(1, 16),
        'I': range(16, 31),
        'N': range(31, 46),
        'G': range(46, 61),
        'O': range(61, 76)
    }

    card = [[] for _ in range(5)]
    for col, column in enumerate(column_ranges.keys()):
        col_numbers = [n for n in numbers if n in column_ranges[column]]
        if len(col_numbers) != 5:
            raise ValueError(f"not valid for column {column}")
        card[col] = col_numbers

    card[2][2] = None  # Free space
    return card


def mark_number(card, number):
    if number < 1 or number > 75:
        raise ValueError("number must be between 1 and 75")
    for row in card:
        for i in range(len(row)):
            if row[i] == number:
                row[i] = None
                return True
    return False


def has_won(card):
    # Check rows
    for row in card:
        if all(num is None for num in row):
            return True
    # Check columns
    for col in range(5):
        if all(card[row][col] is None for row in range(5)):
            return True
    # Check diagonals
    if all(card[i][i] is None for i in range(5)):
        return True
    if all(card[i][4 - i] is None for i in range(5)):
        return True
    return False