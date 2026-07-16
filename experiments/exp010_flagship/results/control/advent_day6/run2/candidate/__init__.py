def parse_map(raw_map):
    return [list(line) for line in raw_map.splitlines()]


def locate_guard(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '^':
                return (i, j)
    return None


def trace_walk(grid):
    guard_position = locate_guard(grid)
    if guard_position is None:
        return grid
    guard_row, guard_col = guard_position
    for i in range(guard_row + 1):
        grid[i][guard_col] = 'X'
    return grid


def next_location(grid):
    guard_position = locate_guard(grid)
    if guard_position is None:
        return None
    guard_row, guard_col = guard_position
    return (guard_row - 1, guard_col) if guard_row > 0 else (guard_row, guard_col)