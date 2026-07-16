class World:
    def __init__(self, live_cells=None):
        if live_cells is None:
            live_cells = set()
        self.live_cells = frozenset(live_cells)

    def next_generation(self):
        new_live_cells = set()
        potential_cells = self._get_potential_cells()

        for cell in potential_cells:
            live_neighbors = self._count_live_neighbors(cell)
            if cell in self.live_cells:
                if live_neighbors in (2, 3):
                    new_live_cells.add(cell)
            elif live_neighbors == 3:
                new_live_cells.add(cell)

        return World(new_live_cells)

    def _get_potential_cells(self):
        potential_cells = set(self.live_cells)
        for cell in self.live_cells:
            for neighbor in self._get_neighbors(cell):
                potential_cells.add(neighbor)
        return potential_cells

    def _get_neighbors(self, cell):
        x, y = cell
        return {(x+i, y+j) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)}

    def _count_live_neighbors(self, cell):
        return sum((neighbor in self.live_cells) for neighbor in self._get_neighbors(cell))

    def __repr__(self):
        return f"World({self.live_cells})"

    def __eq__(self, other):
        return self.live_cells == other.live_cells

    def __hash__(self):
        return hash(self.live_cells)

    def render(self, width, height):
        min_x = min(cell[0] for cell in self.live_cells) if self.live_cells else 0
        max_x = max(cell[0] for cell in self.live_cells) if self.live_cells else 0
        min_y = min(cell[1] for cell in self.live_cells) if self.live_cells else 0
        max_y = max(cell[1] for cell in self.live_cells) if self.live_cells else 0

        output = []
        for y in range(min_y, min_y + height):
            row = []
            for x in range(min_x, min_x + width):
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
