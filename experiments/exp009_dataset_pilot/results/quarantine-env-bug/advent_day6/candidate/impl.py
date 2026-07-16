# candidate/impl.py

class GuardPatrolMap:
    def __init__(self, map_text):
        self.grid = self.parse_map(map_text)
        self.guard_position = self.locate_guard()

    def parse_map(self, map_text):
        return [list(line) for line in map_text.strip().split('\n')]

    def locate_guard(self):
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                if cell == '^':
                    return (row_index, col_index)
        return None

    def trace_guard_walk(self):
        if self.guard_position is None:
            return self.grid
        
        row, col = self.guard_position
        for r in range(row + 1):
            self.grid[r][col] = 'X'
        return self.grid

    def next_guard_location(self):
        if self.guard_position is None:
            return None
        row, col = self.guard_position
        return (0, col)

    def get_traced_map(self):
        return [''.join(row) for row in self.grid]
