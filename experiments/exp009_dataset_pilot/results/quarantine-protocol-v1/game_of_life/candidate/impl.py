# candidate/impl.py

class World:
    def __init__(self, live_cells=None):
        if live_cells is None:
            live_cells = set()
        self.live_cells = frozenset(live_cells)

    def next_generation(self):
        new_live_cells = set()
        potential_cells = self.live_cells.union(self._neighbours())
        
        for cell in potential_cells:
            alive = cell in self.live_cells
            neighbour_count = self._count_live_neighbours(cell)
            if alive:
                if neighbour_count in (2, 3):
                    new_live_cells.add(cell)  # survives
            else:
                if neighbour_count == 3:
                    new_live_cells.add(cell)  # becomes alive
        
        return World(new_live_cells)

    def _neighbours(self):
        neighbours = set()
        for cell in self.live_cells:
            x, y = cell
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if (dx, dy) != (0, 0):
                        neighbours.add((x + dx, y + dy))
        return neighbours

    def _count_live_neighbours(self, cell):
        x, y = cell
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (dx, dy) != (0, 0) and (x + dx, y + dy) in self.live_cells:
                    count += 1
        return count

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

    def __eq__(self, other):
        return self.live_cells == other.live_cells

    def __hash__(self):
        return hash(self.live_cells)

    def population(self):
        return len(self.live_cells)

    def __repr__(self):
        return f"World({self.live_cells})"
