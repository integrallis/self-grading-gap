# file: mine_fields/mine_fields.py
import candidate as Constants
from candidate import create_field
from candidate import get_hint
from candidate import place_mine


class MineFields:
    def __init__(self):
        self.field = None

    def create(self, width, height):
        self.field = create_field(width, height)
        return self.field

    def parametrize(self, width, height):
        return self.create(width, height)

    def mine(self, x, y):
        return place_mine(self.field, x, y)

    def get_hint(self, x, y):
        return get_hint(self.field, x, y)
