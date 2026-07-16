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
        self.validate_card(numbers)
        self.grid = self.create_grid(numbers)
        self.marked = [[False] * 5 for _ in range(5)]
        self.marked[2][2] = True  # Center space is free and marked

    @staticmethod
    def number_to_column_letter(number):
        if not (1 <= number <= 75):
            raise ValueError("Number must be between 1 and 75")
        for letter, num_range in BingoCard.COLUMN_RANGES.items():
            if number in num_range:
                return letter
        return None

    @staticmethod
    def validate_card(numbers):
        if len(numbers) != 24:
            raise ValueError("Exactly 24 numbers are required")
        if len(set(numbers)) != 24:
            raise ValueError("Card numbers must be unique")

        for i, (letter, num_range) in enumerate(BingoCard.COLUMN_RANGES.items()):
            column_numbers = numbers[i * 5:(i + 1) * 5]
            for number in column_numbers:
                if number not in num_range:
                    raise ValueError(f"Number {number} not valid for column {letter}")

    @staticmethod
    def create_grid(numbers):
        grid = [[0] * 5 for _ in range(5)]
        index = 0
        for col in range(5):
            for row in range(5):
                if row == 2 and col == 2:
                    continue
                grid[row][col] = numbers[index]
                index += 1
        return grid

    def mark_number(self, number):
        if not (1 <= number <= 75):
            raise ValueError("Number must be between 1 and 75")
        for row in range(5):
            for col in range(5):
                if self.grid[row][col] == number:
                    self.marked[row][col] = True
                    return True
        return False

    def check_bingo(self):
        # Check rows
        for row in range(5):
            if all(self.marked[row]) or (row == 2 and sum(self.marked[row]) == 4):
                return True
        
        # Check columns
        for col in range(5):
            if all(self.marked[row][col] for row in range(5)):
                return True
        
        # Check diagonals
        if all(self.marked[i][i] for i in range(5)) or all(self.marked[i][4 - i] for i in range(5)):
            return True
        
        return False
