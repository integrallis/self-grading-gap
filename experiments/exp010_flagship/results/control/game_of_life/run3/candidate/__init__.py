class World:
    def __init__(self, live_cells):
        self.live_cells = set(live_cells)

    def evolve(self):
        new_cells = set()
        potential_cells = self.live_cells.copy()

        # Add neighbors of live cells to potential cells
        for cell in self.live_cells:
            potential_cells.update(self.get_neighbors(cell))

        for cell in potential_cells:
            count = self.neighbour_count(cell)
            if cell in self.live_cells:
                # Cell is alive
                if count == 2 or count == 3:
                    new_cells.add(cell)  # Survives
            else:
                # Cell is dead
                if count == 3:
                    new_cells.add(cell)  # Becomes alive

        return World(new_cells)

    def neighbour_count(self, cell):
        return sum((neighbor in self.live_cells) for neighbor in self.get_neighbors(cell))

    def get_neighbors(self, cell):
        x, y = cell
        return {(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)}

    @classmethod
    def from_text(cls, text):
        live_cells = {(i, j) for i, row in enumerate(text) for j, char in enumerate(row) if char == '*'}
        return cls(live_cells)

    def render(self, width, height):
        return [''.join('*' if (x, y) in self.live_cells else '.' for x in range(width)) for y in range(height)]

    def __eq__(self, other):
        return self.live_cells == other.live_cells

    def __hash__(self):
        return hash(frozenset(self.live_cells))