# candidate/impl.py

class BingoCard:
    def __init__(self, numbers):
        self.validate_card(numbers)
        self.grid = self.create_grid(numbers)
        self.marked = [[False] * 5 for _ in range(5)]
        self.marked[2][2] = True  # Free space in the center

    @staticmethod
    def validate_card(numbers):
        if len(numbers) != 24:
            raise ValueError("exactly 24 numbers are required")
        if len(set(numbers)) != 24:
            raise ValueError("card numbers must be unique")
        column_ranges = {
            0: range(1, 16),    # B
            1: range(16, 31),   # I
            2: range(31, 46),   # N
            3: range(46, 61),   # G
            4: range(61, 76),   # O
        }
        for col in range(5):
            for number in numbers[col * 5:(col + 1) * 5]:
                if number not in column_ranges[col]:
                    raise ValueError(f"number {number} not valid for column {['B', 'I', 'N', 'G', 'O'][col]}")

    @staticmethod
    def create_grid(numbers):
        grid = [[0] * 5 for _ in range(5)]
        idx = 0
        for col in range(5):
            for row in range(5):
                if row == 2 and col == 2:
                    continue  # Skip free space
                grid[row][col] = numbers[idx]
                idx += 1
        return grid

    @staticmethod
    def get_column_letter(number):
        if not (1 <= number <= 75):
            raise ValueError("number must be between 1 and 75")
        if number <= 15:
            return 'B'
        elif number <= 30:
            return 'I'
        elif number <= 45:
            return 'N'
        elif number <= 60:
            return 'G'
        else:
            return 'O'

    def mark_number(self, number):
        if not (1 <= number <= 75):
            raise ValueError("number must be between 1 and 75")
        for row in range(5):
            for col in range(5):
                if self.grid[row][col] == number:
                    self.marked[row][col] = True
                    return True
        return False

    def check_win(self):
        # Check rows
        for row in self.marked:
            if all(row):
                return True
        # Check columns
        for col in range(5):
            if all(self.marked[row][col] for row in range(5)):
                return True
        # Check diagonals
        if all(self.marked[i][i] for i in range(5)):
            return True
        if all(self.marked[i][4 - i] for i in range(5)):
            return True
        return False
