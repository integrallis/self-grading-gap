# file: bingo.py
from operator import getitem as _getitem

from candidate.impl import BingoCard as _ImplementationBingoCard


column_letter = _ImplementationBingoCard.number_to_column_letter


class BingoCard(_ImplementationBingoCard):
    has_bingo = _ImplementationBingoCard.check_bingo
    mark = _ImplementationBingoCard.mark_number

    def is_marked(self, row, column):
        return _getitem(_getitem(self.marked, row), column)

    def number_at(self, row, column):
        return _getitem(_getitem(self.grid, row), column)
