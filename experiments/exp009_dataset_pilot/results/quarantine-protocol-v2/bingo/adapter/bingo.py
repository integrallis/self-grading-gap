from bingo import BingoCard
from bingo import column_letter

class BingoCard:
    COLUMN_RANGES = {
        'B': range(1, 16),
        'I': range(16, 31),
        'N': range(31, 46),
        'G': range(46, 61),
        'O': range(61, 76)
    }
    
    def __init__(self, numbers):
        self.card = [[None] * 5 for _ in range(5)]
        self.marked = [[False] * 5 for _ in range(5)]
        self.validate_card(numbers)
        self.fill_card(numbers)
        self.marked[2][2] = True  # Center space is free and pre-marked

    def validate_card(self, numbers):
        self.check_length(numbers)
        self.check_uniqueness(numbers)
        self.check_ranges(numbers)

    def check_length(self, numbers):
        if len(numbers) != 24:
            raise ValueError("exactly 24 numbers are required")

    def check_uniqueness(self, numbers):
        if len(set(numbers)) != len(numbers):
            raise ValueError("card numbers must be unique")

    def check_ranges(self, numbers):
        for i, (col, rng) in enumerate(zip('BINGO', self.COLUMN_RANGES.values())):
            for j in range(5):
                if j == 2 and col == 'N':  # Skip center space for N
                    continue
                if numbers[i * 5 + j] not in rng:
                    raise ValueError(f"number {numbers[i * 5 + j]} is not valid for column {col}")

    def fill_card(self, numbers):
        index = 0
        for col in range(5):
            for row in range(5):
                if col == 2 and row == 2:  # Skip center space
                    continue
                self.card[row][col] = numbers[index]
                index += 1

    def call_number(self, number):
        if not 1 <= number <= 75:
            raise ValueError("number must be between 1 and 75")
        
        for row in range(5):
            for col in range(5):
                if self.card[row][col] == number:
                    self.marked[row][col] = True
                    return True  # Hit
        return False  # No hit

    def check_win(self):
        for i in range(5):
            if all(self.marked[i]) or all(self.marked[j][i] for j in range(5)):
                return True
        
        if all(self.marked[i][i] for i in range(5)) or all(self.marked[i][4 - i] for i in range(5)):
            return True
        
        return False

    @staticmethod
    def get_column_letter(number):
        if not 1 <= number <= 75:
            raise ValueError("number must be between 1 and 75")
        if number in BingoCard.COLUMN_RANGES['B']:
            return 'B'
        elif number in BingoCard.COLUMN_RANGES['I']:
            return 'I'
        elif number in BingoCard.COLUMN_RANGES['N']:
            return 'N'
        elif number in BingoCard.COLUMN_RANGES['G']:
            return 'G'
        elif number in BingoCard.COLUMN_RANGES['O']:
            return 'O'
        else:
            raise ValueError("number must be between 1 and 75")
