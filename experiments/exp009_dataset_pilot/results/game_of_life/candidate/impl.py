# candidate/impl.py

class World:
    def __init__(self, live_cells=None):
        self.live_cells = frozenset(live_cells) if live_cells else frozenset()

    def next_generation(self):
        new_live_cells = set()
        potential_cells = self._get_potential_cells()
        
        for cell in potential_cells:
            live_neighbors = self._live_neighbor_count(cell)
            if cell in self.live_cells:
                if live_neighbors == 2 or live_neighbors == 3:
                    new_live_cells.add(cell)  # Survival
            else:
                if live_neighbors == 3:
                    new_live_cells.add(cell)  # Birth
        
        return World(new_live_cells)

    def _get_potential_cells(self):
        neighbors = set()
        for cell in self.live_cells:
            neighbors.add(cell)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx != 0 or dy != 0:
                        neighbors.add((cell[0] + dx, cell[1] + dy))
        return neighbors

    def _live_neighbor_count(self, cell):
        count = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx != 0 or dy != 0:
                    neighbor = (cell[0] + dx, cell[1] + dy)
                    if neighbor in self.live_cells:
                        count += 1
        return count

    def render(self, width, height):
        output = []
        for y in range(height):
            row = []
            for x in range(width):
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
            for x, cell in enumerate(row):
                if cell == '*':
                    live_cells.add((x, y))
        return cls(live_cells)

    def __eq__(self, other):
        return self.live_cells == other.live_cells

    def __hash__(self):
        return hash(self.live_cells)

    def population(self):
        return len(self.live_cells)

    def is_empty(self):
        return not self.live_cells

    def __repr__(self):
        return f"World({self.live_cells})"
