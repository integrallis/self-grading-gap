# file: game_of_life.py
from candidate import World as _World


class Grid(_World):
    def __init__(self, live_cells=()):
        super().__init__(live_cells)

    @classmethod
    def from_rows(cls, rows):
        return cls.from_text(rows)

    def is_alive(self, x, y):
        return self.live_cells.__contains__((x, y))

    def join(self, other):
        return type(self)(self.live_cells.union(other.live_cells))

    def live_neighbours(self, x, y):
        return self.neighbour_count((x, y))

    def next_generation(self):
        return type(self)(self.evolve().live_cells)
