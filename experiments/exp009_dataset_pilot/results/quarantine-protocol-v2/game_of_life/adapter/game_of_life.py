# candidate/impl.py
from game_of_life import Grid

class World:
    def __init__(self, live_cells=None):
        if live_cells is None:
            self.live_cells = frozenset()
        else:
            self.live_cells = frozenset(live_cells)

    def __eq__(self, other):
        if not isinstance(other, World):
            return NotImplemented
        return self.live_cells == other.live_cells

    def __hash__(self):
        return hash(self.live_cells)

    def next_generation(self):
        new_live_cells = set()
        candidates = self.live_cells.copy()

        for cell in self.live_cells:
            neighbors = self._get_neighbors(cell)
            live_neighbors = self._count_live_neighbors(neighbors)
            
            if live_neighbors in (2, 3):
                new_live_cells.add(cell)

            candidates.update(neighbors)

        for cell in candidates:
            if cell not in self.live_cells:
                if self._count_live_neighbors(self._get_neighbors(cell)) == 3:
                    new_live_cells.add(cell)

        return World(new_live_cells)

    def _get_neighbors(self, cell):
        x, y = cell
        return {(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)}

    def _count_live_neighbors(self, neighbors):
        return sum((neighbor in self.live_cells) for neighbor in neighbors)

    def render(self, width, height):
        output = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append('*' if (x, y) in self.live_cells else '.')
            output.append(''.join(row))
        return '\n'.join(output)

    @classmethod
    def from_rows(cls, rows):
        live_cells = set()
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                if char == '*':
                    live_cells.add((x, y))
        return cls(live_cells)

    def __str__(self):
        if not self.live_cells:
            return 'Empty World'
        min_x = min(x for x, y in self.live_cells)
        max_x = max(x for x, y in self.live_cells)
        min_y = min(y for x, y in self.live_cells)
        max_y = max(y for x, y in self.live_cells)
        return self.render(max_x - min_x + 1, max_y - min_y + 1)

# Example usage of the World class
if __name__ == "__main__":
    initial_pattern = [
        ".....",
        "..*..",
        "..*..",
        "..*..",
        "....."
    ]
    world = World.from_rows(initial_pattern)
    print("Initial World:")
    print(world)
    next_world = world.next_generation()
    print("Next Generation:")
    print(next_world)
