# candidate/impl.py

class BingoCard:
    COLUMN_RANGES = {
        'B': range(1, 16),
        'I': range(16, 31),
        'N': range(31, 46),
        'G': range(46, 61),
        'O': range(61, 76)
    }

    def __init__(self, numbers):
        self.card = self.validate_card(numbers)
        self.marked = [[False] * 5 for _ in range(5)]
        self.marked[2][2] = True  # Center space is free and marked

    @staticmethod
    def get_column_letter(number):
        if number < 1 or number > 75:
            raise ValueError("Number must be between 1 and 75")
        for letter, rng in BingoCard.COLUMN_RANGES.items():
            if number in rng:
                return letter
        return None

    @classmethod
    def validate_card(cls, numbers):
        if len(numbers) != 24:
            raise ValueError("exactly 24 numbers are required")
        if len(set(numbers)) != 24:
            raise ValueError("card numbers must be unique")
        for i, (letter, rng) in enumerate(cls.COLUMN_RANGES.items()):
            for j in range(5):
                if j == 2 and letter == 'N':
                    continue  # Skip center space
                if numbers[i * 5 + j] not in rng:
                    raise ValueError(f"number not valid for column {letter}")
        return cls.arrange_numbers(numbers)

    @staticmethod
    def arrange_numbers(numbers):
        card = [[0] * 5 for _ in range(5)]
        index = 0
        for col in range(5):
            for row in range(5):
                if row == 2 and col == 2:
                    card[row][col] = None  # Center space
                else:
                    card[row][col] = numbers[index]
                    index += 1
        return card

    def mark_number(self, number):
        if number < 1 or number > 75:
            raise ValueError("Number must be between 1 and 75")
        for row in range(5):
            for col in range(5):
                if self.card[row][col] == number:
                    self.marked[row][col] = True
                    return True
        return False

    def check_win(self):
        # Check rows and columns
        for i in range(5):
            if all(self.marked[i]) or all(self.marked[j][i] for j in range(5)):
                return True
        # Check diagonals
        if all(self.marked[i][i] for i in range(5)) or all(self.marked[i][4 - i] for i in range(5)):
            return True
        return False
