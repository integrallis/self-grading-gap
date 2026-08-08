# file: mine_fields/mine_fields.py
import candidate as Constants

from candidate import create_field, get_cell_hint, place_mine


class MineFields:
    def create(self, width, height):
        self._field = create_field(width, height)
        return self._field

    def parametrize(self, width, height):
        return self.create(width, height)

    def mine(self, x, y):
        return place_mine(self._field, x, y)

    def get_hint(self, x, y):
        return get_cell_hint(self._field, x, y)
