class World:
    def __init__(self, live_cells):
        self.live_cells = frozenset(live_cells)

    def evolve(self):
        new_live_cells = set()
        candidates = self.live_cells.union(
            (x + dx, y + dy)
            for x, y in self.live_cells
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
        )
        for cell in candidates:
            live_neighbors = self.live_neighbours_count(cell)
            if cell in self.live_cells:
                if live_neighbors in (2, 3):
                    new_live_cells.add(cell)
            else:
                if live_neighbors == 3:
                    new_live_cells.add(cell)
        return World(new_live_cells)

    def live_neighbours_count(self, cell):
        x, y = cell
        return sum((x + dx, y + dy) in self.live_cells
                   for dx in (-1, 0, 1)
                   for dy in (-1, 0, 1) if (dx, dy) != (0, 0))

    @classmethod
    def from_text(cls, lines):
        live_cells = set()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '*':
                    live_cells.add((y, x))  # (row, column)
        return cls(live_cells)

    def render_window(self, height, width):
        output = []
        for y in range(height):
            line = ''.join('*' if (y, x) in self.live_cells else '.' for x in range(width))
            output.append(line)
        return '\n'.join(output)  # Proper newline character

    def __eq__(self, other):
        return self.live_cells == other.live_cells

    def __hash__(self):
        return hash(self.live_cells)