# file: bingo.py

from candidate.impl import BingoCard as ImplBingoCard

class BingoCard(ImplBingoCard):
    def __init__(self, numbers):
        super().__init__(numbers)

    @staticmethod
    def get_column_letter(number):
        return ImplBingoCard.get_column_letter(number)

    def mark_number(self, number):
        return super().mark_number(number)

    def check_win(self):
        return super().check_win()

def column_letter(number):
    return BingoCard.get_column_letter(number)
