# file: mine_fields/mine_fields.py
import candidate as Constants
from candidate import create_field, get_hint, place_mines


class MineFields:
    def create(self, rows, cols):
        self.field = create_field(rows, cols)
        return self.field

    def mine(self, row, col):
        return place_mines(self.field, ((row, col),))

    def get_hint(self, row, col):
        return get_hint(self.field, row, col)

    def parametrize(self, rows, cols):
        return self.create(rows, cols)
