class World:
    def __init__(self, live_cells=None):
        if live_cells is None:
            self.live_cells = frozenset()
        else:
            self.live_cells = frozenset(live_cells)

    def __eq__(self, other):
        return self.live_cells == other.live_cells

    def __hash__(self):
        return hash(self.live_cells)

    def step(self):
        new_live_cells = set()
        candidates = self._get_candidates()
        for cell in candidates:
            live_neighbors = self._count_live_neighbors(cell)
            if cell in self.live_cells:
                if live_neighbors in (2, 3):
                    new_live_cells.add(cell)
            elif live_neighbors == 3:
                new_live_cells.add(cell)
        return World(new_live_cells)

    def _get_candidates(self):
        candidates = set()
        for cell in self.live_cells:
            candidates.add(cell)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if (dx, dy) != (0, 0):
                        candidates.add((cell[0] + dx, cell[1] + dy))
        return candidates

    def _count_live_neighbors(self, cell):
        count = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if (dx, dy) != (0, 0):
                    neighbor = (cell[0] + dx, cell[1] + dy)
                    if neighbor in self.live_cells:
                        count += 1
        return count

    def render(self, width, height):
        min_x = min(x for x, _ in self.live_cells) if self.live_cells else 0
        min_y = min(y for _, y in self.live_cells) if self.live_cells else 0
        output = []
        for y in range(min_y, min_y + height):
            row = []
            for x in range(min_x, min_x + width):
                if (x, y) in self.live_cells:
                    row.append('*')
                else:
                    row.append('.')
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
