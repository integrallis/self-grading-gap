# file: game_of_life.py
from candidate.impl import World

class Grid:
    def __init__(self, live_cells=None):
        self.world = World(live_cells)

    def next_generation(self):
        self.world = self.world.next_generation()

    def render(self, width, height):
        return self.world.render(width, height)

    @classmethod
    def from_rows(cls, rows):
        return cls(World.from_rows(rows).live_cells)

    def __repr__(self):
        return repr(self.world)

    def __eq__(self, other):
        return self.world == other.world

    def __hash__(self):
        return hash(self.world)
