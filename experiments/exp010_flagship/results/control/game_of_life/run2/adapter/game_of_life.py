# file: game_of_life.py
from candidate import World


def _from_rows(cls, rows):
    return cls(rows)


def _is_alive(self, x, y):
    return self.live_cells().__contains__((x, y))


def _join(self, separator):
    return separator.join(self.to_text())


def _live_neighbours(self, x, y):
    return self.live_neighbours_count((x, y))


World.from_rows = classmethod(_from_rows)
World.is_alive = _is_alive
World.join = _join
World.live_neighbours = _live_neighbours
World.next_generation = World.advance

Grid = World
