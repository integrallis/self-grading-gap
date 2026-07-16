# file: game_of_life.py
from candidate import World


class Grid(World):
    def __init__(self, live_cells=()):
        super().__init__(live_cells)

    @classmethod
    def from_rows(cls, rows):
        return cls.from_text(rows)

    def is_alive(self, row, column):
        return self.live_cells.__contains__((row, column))

    def join(self, other):
        return type(self)(self.live_cells.union(other.live_cells))

    def live_neighbours(self, row, column):
        return self.live_neighbours_count((row, column))

    def next_generation(self):
        return self.evolve()

    def render(self, height, width):
        return self.render_window(height, width)
