class World:
    def __init__(self, live_cells=None):
        self.live_cells_set = live_cells if live_cells is not None else set()

    def population(self):
        return len(self.live_cells_set)

    def live_cells(self):
        return self.live_cells_set

    def advance(self):
        new_cells = set()
        potential_cells = set()

        for cell in self.live_cells_set:
            potential_cells.add(cell)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (dx, dy) != (0, 0):
                        potential_cells.add((cell[0] + dx, cell[1] + dy))

        for cell in potential_cells:
            count = self.live_neighbours_count(cell)
            if cell in self.live_cells_set:
                if count in {2, 3}:
                    new_cells.add(cell)  # Survive
            else:
                if count == 3:
                    new_cells.add(cell)  # Become alive

        return World(new_cells)

    def live_neighbours_count(self, cell):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx, dy) != (0, 0):
                    neighbor = (cell[0] + dx, cell[1] + dy)
                    if neighbor in self.live_cells_set:
                        count += 1
        return count

    def to_text(self):
        if not self.live_cells_set:
            return ['.']  # Represents an empty world
        min_x = min(cell[0] for cell in self.live_cells_set)
        max_x = max(cell[0] for cell in self.live_cells_set)
        min_y = min(cell[1] for cell in self.live_cells_set)
        max_y = max(cell[1] for cell in self.live_cells_set)

        grid = []
        for x in range(min_x, max_x + 1):
            row = []
            for y in range(min_y, max_y + 1):
                row.append('*' if (x, y) in self.live_cells_set else '.')
            grid.append(''.join(row))
        return grid

    def render(self, width, height):
        grid = [['.' for _ in range(width)] for _ in range(height)]
        for (x, y) in self.live_cells_set:
            if 0 <= x < height and 0 <= y < width:
                grid[x][y] = '*'
        return [''.join(row) for row in grid]

    def __eq__(self, other):
        return self.live_cells_set == other.live_cells_set

    def __hash__(self):
        return hash(frozenset(self.live_cells_set))