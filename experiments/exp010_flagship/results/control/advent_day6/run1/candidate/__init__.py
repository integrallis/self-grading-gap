def parse_map(input_map):
    return [list(line) for line in input_map.split('\n')]


def locate_guard(input_map):
    grid = parse_map(input_map)
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == '^':
                return (r, c)
    return ()


def trace_guard_walk(input_map):
    grid = parse_map(input_map)
    guard_pos = locate_guard(input_map)
    if not guard_pos:
        return grid
    r, c = guard_pos
    # Assume the guard can only move up in this implementation
    if r > 0:
        grid[r][c] = '.'  # Clear the current guard position
        grid[r-1][c] = 'X'  # Mark the new position
    return grid


def report_next_location(input_map):
    guard_pos = locate_guard(input_map)
    if not guard_pos:
        return ()
    r, c = guard_pos
    return (r - 1, c) if r > 0 else ()