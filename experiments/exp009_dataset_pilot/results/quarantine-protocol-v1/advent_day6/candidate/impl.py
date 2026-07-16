# candidate/impl.py

class GuardPatrolMap:
    def __init__(self, map_text):
        self.grid = self.parse_map(map_text)
        self.guard_position = self.find_guard_position()

    def parse_map(self, map_text):
        """Parse the input map text into a grid."""
        return [list(line) for line in map_text.splitlines()]

    def find_guard_position(self):
        """Locate the guard's position on the grid."""
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == '^':
                    return (r, c)
        return None

    def trace_guard_walk(self):
        """Trace the guard's walk and return a marked grid."""
        if self.guard_position is None:
            return self.grid
        
        r, c = self.guard_position
        for i in range(r + 1):
            self.grid[i][c] = 'X'
        return self.grid

    def next_guard_location(self):
        """Get the next location of the guard if it moves up."""
        if self.guard_position is None:
            return None
        
        r, c = self.guard_position
        next_row = max(r - 1, 0)
        return (next_row, c)

# Example usage:
# map_text = """..^
#                ..
#                .."""
# patrol = GuardPatrolMap(map_text)
# print(patrol.trace_guard_walk())
# print(patrol.next_guard_location())
