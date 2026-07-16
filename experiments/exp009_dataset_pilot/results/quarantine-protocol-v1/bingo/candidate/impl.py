# candidate/impl.py

class BingoCard:
    COLUMNS = {
        'B': range(1, 16),
        'I': range(16, 31),
        'N': range(31, 46),
        'G': range(46, 61),
        'O': range(61, 76)
    }

    def __init__(self, numbers):
        if len(numbers) != 24:
            raise ValueError("exactly 24 numbers are required")
        if len(set(numbers)) != 24:
            raise ValueError("card numbers must be unique")
        
        self.card = [[None] * 5 for _ in range(5)]
        self.marked = [[False] * 5 for _ in range(5)]
        self.marked[2][2] = True  # Free space in the center
        
        for col_index, (col_letter, col_range) in enumerate(self.COLUMNS.items()):
            col_numbers = [num for num in numbers if num in col_range]
            if len(col_numbers) != 5 - (1 if col_letter == 'N' else 0):  # N has 4 numbers
                raise ValueError(f"{col_letter} column must have numbers within its range")
            for row_index in range(len(col_numbers)):
                self.card[row_index if col_letter != 'N' else row_index + 1][col_index] = col_numbers[row_index]

    @staticmethod
    def get_column_letter(number):
        if not (1 <= number <= 75):
            raise ValueError("number must be between 1 and 75")
        for letter, number_range in BingoCard.COLUMNS.items():
            if number in number_range:
                return letter

    def mark_number(self, number):
        if not (1 <= number <= 75):
            raise ValueError("number must be between 1 and 75")
        for row in range(5):
            for col in range(5):
                if self.card[row][col] == number:
                    self.marked[row][col] = True
                    return True
        return False

    def check_win(self):
        # Check rows
        for row in range(5):
            if all(self.marked[row]) or (row == 2 and sum(self.marked[row]) == 4):
                return True
        # Check columns
        for col in range(5):
            if all(self.marked[row][col] for row in range(5) if not (row == 2 and col == 2)) or \
               (col == 2 and sum(self.marked[row][col] for row in range(5)) == 4):
                return True
        # Check diagonals
        if all(self.marked[i][i] for i in range(5) if not (i == 2)) or \
           all(self.marked[i][4 - i] for i in range(5) if not (i == 2)):
            return True
        return False
