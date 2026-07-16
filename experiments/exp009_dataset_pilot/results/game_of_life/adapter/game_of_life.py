# file: game_of_life.py
from candidate.impl import World


class Grid(World):
    @classmethod
    def from_rows(cls, rows):
        return cls(World.from_rows(rows).live_cells)

    def is_alive(self, x, y):
        return self.live_cells.__contains__((x, y))

    def live_neighbours(self, x, y):
        return self._live_neighbor_count((x, y))

    def join(self, other):
        return Grid(self.live_cells.union(other.live_cells))

    def next_generation(self):
        return Grid(World.next_generation(self).live_cells)
