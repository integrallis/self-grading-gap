# candidate/impl.py

class GuardPatrolMap:
    def __init__(self, map_text):
        self.grid = self.parse_grid(map_text)
        self.guard_position = self.find_guard_position()

    def parse_grid(self, map_text):
        return [list(line) for line in map_text.splitlines()]

    def find_guard_position(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == '^':
                    return (row, col)
        return None

    def trace_guard_walk(self):
        if self.guard_position is None:
            return self.grid
        
        guard_row, guard_col = self.guard_position
        for row in range(guard_row + 1):
            self.grid[row][guard_col] = 'X'
        return self.grid

    def get_next_location(self):
        if self.guard_position is None:
            return None
        guard_row, guard_col = self.guard_position
        return (0, guard_col)

    def get_traced_map(self):
        traced_map = self.trace_guard_walk()
        return '\n'.join([''.join(row) for row in traced_map])
