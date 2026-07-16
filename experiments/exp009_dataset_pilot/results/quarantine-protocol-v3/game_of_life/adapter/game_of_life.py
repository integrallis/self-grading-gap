# file: game_of_life.py
from candidate.impl import World


class Grid(World):
    def is_alive(self, x, y):
        return self.live_cells.__contains__((x, y))

    def live_neighbours(self, x, y):
        return self._count_live_neighbors((x, y))

    def next_generation(self):
        return self.__class__(self.step().live_cells)

    def join(self, other):
        return self.__class__(self.live_cells.union(other.live_cells))
