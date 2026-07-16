# file: bingo.py
from candidate import announce_column
from candidate import create_card
from candidate import has_won
from candidate import mark_number


column_letter = announce_column


class BingoCard:
    def __init__(self, numbers):
        self._card = create_card(numbers)

    def has_bingo(self):
        return has_won(self._card)

    def is_marked(self, row, column):
        return self.number_at(row, column).__eq__(None)

    def mark(self, number):
        return mark_number(self._card, number)

    def number_at(self, row, column):
        return self._card.__getitem__(column).__getitem__(row)
