# file: bingo.py
from candidate.impl import BingoCard as _BingoCard


class BingoCard(_BingoCard):
    mark = _BingoCard.mark_number
    has_bingo = _BingoCard.check_win

    def number_at(self, row, column):
        return self.grid.__getitem__(row).__getitem__(column)

    def is_marked(self, row, column):
        return self.marked.__getitem__(row).__getitem__(column)


column_letter = _BingoCard.get_column_letter
