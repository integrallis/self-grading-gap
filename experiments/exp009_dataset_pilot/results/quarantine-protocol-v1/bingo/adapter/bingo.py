# file: bingo.py

from candidate.impl import BingoCard as _BingoCard
from candidate.impl import BingoCard as _get_column_letter

class BingoCard(_BingoCard):
    def __init__(self, numbers):
        super().__init__(numbers)

    def mark_number(self, number):
        return super().mark_number(number)

    def check_win(self):
        return super().check_win()

def column_letter(number):
    return _get_column_letter.get_column_letter(number)
