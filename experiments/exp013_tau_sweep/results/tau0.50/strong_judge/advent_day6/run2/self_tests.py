# test_guard_patrol.py

from solution import parse_map, locate_guard, trace_guard_walk, next_guard_location

def test_parse_map():
    # Test input map with various characters
    input_map = "...\n#.#\n..."
    expected_output = [['.', '.', '.'], ['#', '.', '#'], ['.', '.', '.']]
    assert parse_map(input_map) == expected_output

    # Test input map with additional characters (spaces)
    input_map = " . . \n# # #\n . . "
    expected_output = [[' ', '.', ' ', '.', ' '], ['#', ' ', '#', ' ', '#'], [' ', '.', ' ', '.', ' ']]
    assert parse_map(input_map) == expected_output

def test_locate_guard():
    # Test grid with guard located on the top row
    grid = [['.', '.', '^'], ['#', '#', '#'], ['.', '.', '.']]
    expected_position = (0, 2)  # Row 0, Column 2
    assert locate_guard(grid) == expected_position

    # Test grid with guard located in the middle row
    grid = [['.', '.', '.'], ['#', '^', '#'], ['.', '.', '.']]
    expected_position = (1, 1)  # Row 1, Column 1
    assert locate_guard(grid) == expected_position

    # Test grid with guard located on the bottom row
    grid = [['.', '.', '.'], ['#', '#', '#'], ['.', '^', '.']]
    expected_position = (2, 1)  # Row 2, Column 1
    assert locate_guard(grid) == expected_position

    # Test grid without guard
    grid = [['.', '.', '.'], ['#', '#', '#'], ['.', '.', '.']]
    assert not locate_guard(grid)  # No guard present

def test_trace_guard_walk():
    # Test grid with guard walking from middle row
    grid = [['.', '.', '.'], ['#', '^', '#'], ['.', '.', '.']]
    expected_traced_grid = [['.', 'X', '.'], ['#', 'X', '#'], ['.', '.', '.']]  # Guard occupies (1, 1) and (0, 1)
    assert trace_guard_walk(grid) == expected_traced_grid

    # Test grid with guard on the top row
    grid = [['.', '.', '^'], ['#', '#', '#'], ['.', '.', '.']]
    expected_traced_grid = [['.', '.', 'X'], ['#', '#', '#'], ['.', '.', '.']]  # Only (0, 2) becomes 'X'
    assert trace_guard_walk(grid) == expected_traced_grid

    # Test grid with guard on the bottom row in a two-row grid
    grid = [['.', '.', '.'], ['#', '#', '^']]
    expected_traced_grid = [['.', '.', 'X'], ['#', '#', 'X']]  # Both cells (1, 2) and (0, 2) become 'X'
    assert trace_guard_walk(grid) == expected_traced_grid

    # Test grid without guard
    grid = [['.', '.', '.'], ['#', '#', '#'], ['.', '.', '.']]
    expected_traced_grid = [['.', '.', '.'], ['#', '#', '#'], ['.', '.', '.']]
    assert trace_guard_walk(grid) == expected_traced_grid

    # Verify input grid remains unchanged after tracing
    original_grid = [['.', '.', '^'], ['#', '#', '#'], ['.', '.', '.']]
    trace_guard_walk(original_grid)  # Call the function
    assert original_grid == [['.', '.', '^'], ['#', '#', '#'], ['.', '.', '.']]  # Check original is unchanged

def test_next_guard_location():
    # Test next location for guard at row 1, column 1
    grid = [['.', '.', '.'], ['#', '^', '#'], ['.', '.', '.']]
    expected_next_location = (0, 1)  # Next location is Row 0, Column 1
    assert next_guard_location(grid) == expected_next_location

    # Test next location for guard at row 0, column 2
    grid = [['.', '.', '^'], ['#', '#', '#'], ['.', '.', '.']]
    expected_next_location = (0, 2)  # Same location, as guard is at the top
    assert next_guard_location(grid) == expected_next_location