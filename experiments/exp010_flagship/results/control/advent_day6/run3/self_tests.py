# test_guard_patrol.py

from solution import parse_map, locate_guard, trace_guard_walk, report_next_location

def test_parse_map():
    # Given a raw map text
    raw_map = "...\n.#.\n..."
    # The expected grid is a list of lists, where each sub-list is a row of characters
    expected_grid = [['.', '.', '.'], ['.', '#', '.'], ['.', '.', '.']]
    # Test if the function correctly parses the map
    assert parse_map(raw_map) == expected_grid

def test_locate_guard():
    # Given a grid with a guard
    grid_with_guard = [['.', '.', '.'], ['.', '^', '.'], ['.', '.', '.']]
    # The guard is located at row 1, column 1
    expected_position = (1, 1)  # (row, column)
    # Test if the function locates the guard correctly
    assert locate_guard(grid_with_guard) == expected_position

def test_locate_guard_no_guard():
    # Given a grid with no guard
    grid_no_guard = [['.', '.', '.'], ['.', '#', '.'], ['.', '.', '.']]
    # The expected position report is empty
    expected_position = ()
    # Test if the function reports no position correctly
    assert locate_guard(grid_no_guard) == expected_position

def test_trace_guard_walk():
    # Given a grid with a guard at row 1, column 1
    grid_with_guard = [['.', '.', '.'], ['.', '^', '.'], ['.', '.', '.']]
    # The guard will walk straight up to the top edge, marking only its own position
    expected_traced_grid = [['.', 'X', '.'], ['.', '.', '.'], ['.', '.', '.']]
    # Test if the function traces the guard's walk correctly
    assert trace_guard_walk(grid_with_guard) == expected_traced_grid

def test_trace_guard_walk_no_guard():
    # Given a grid with no guard
    grid_no_guard = [['.', '.', '.'], ['.', '#', '.'], ['.', '.', '.']]
    # The traced grid should be identical to the input grid
    expected_traced_grid = [['.', '.', '.'], ['.', '#', '.'], ['.', '.', '.']]
    # Test if the function returns the original grid correctly
    assert trace_guard_walk(grid_no_guard) == expected_traced_grid

def test_report_next_location():
    # Given a grid with a guard at row 0, column 1
    grid_with_guard = [['.', '^', '.'], ['.', '#', '.'], ['.', '.', '.']]
    # The next location for the guard is row 0, column 1
    expected_next_location = (0, 1)  # (row, column)
    # Test if the function reports the next location correctly
    assert report_next_location(grid_with_guard) == expected_next_location

def test_guard_at_top_row():
    # Given a grid with a guard at the top row
    grid_with_guard = [['^', '.', '.'], ['.', '#', '.'], ['.', '.', '.']]
    # The guard will walk straight up, marking only its own position
    expected_traced_grid = [['X', '.', '.'], ['.', '#', '.'], ['.', '.', '.']]
    assert trace_guard_walk(grid_with_guard) == expected_traced_grid

def test_guard_at_bottom_row():
    # Given a grid with a guard at the bottom row
    grid_with_guard = [['.', '.', '.'], ['.', '#', '.'], ['.', '.', '^']]
    # The guard will walk straight up to the top edge, marking all cells in its column
    expected_traced_grid = [['.', '.', 'X'], ['.', '#', 'X'], ['.', '.', 'X']]
    assert trace_guard_walk(grid_with_guard) == expected_traced_grid