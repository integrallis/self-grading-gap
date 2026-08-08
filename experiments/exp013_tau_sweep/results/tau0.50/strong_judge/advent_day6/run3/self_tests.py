# test_solution.py

from solution import parse_map, locate_guard, trace_walk, next_location

def test_parse_map_single_line():
    # Input: ".#."
    # Expected output: [['.', '#', '.']]
    assert parse_map(".#.") == [['.', '#', '.']]

def test_parse_map_multiple_lines():
    # Input: ".#.\n..#"
    # Expected output: [['.', '#', '.'], ['.', '.', '#']]
    assert parse_map(".#.\n..#") == [['.', '#', '.'], ['.', '.', '#']]

def test_parse_map_with_spaces():
    # Input: ". # .\n..#"
    # Expected output: [['.', ' ', '#', ' ', '.'], ['.', '.', '#']]
    assert parse_map(". # .\n..#") == [['.', ' ', '#', ' ', '.'], ['.', '.', '#']]

def test_parse_map_with_empty_intermediate_line():
    # Input: ".\n\n#"
    # Expected output: [['.'], [], ['#']] with an empty row in between
    assert parse_map(".\n\n#") == [['.'], [], ['#']]

def test_locate_guard_present_top_row():
    # Input: [['^', '#', '.'], ['.', '.', '#']]
    # Expected output: (0, 0) since the guard is at row 0, column 0
    assert locate_guard([['^', '#', '.'], ['.', '.', '#']]) == (0, 0)

def test_locate_guard_present_interior_row():
    # Input: [['.', '#', '.'], ['^', '.', '#']]
    # Expected output: (1, 0) since the guard is at row 1, column 0
    assert locate_guard([['.', '#', '.'], ['^', '.', '#']]) == (1, 0)

def test_locate_guard_present_bottom_row():
    # Input: [['.', '#', '.'], ['.', '.', '#'], ['^', '.', '#']]
    # Expected output: (2, 0) since the guard is at row 2, column 0
    assert locate_guard([['.', '#', '.'], ['.', '.', '#'], ['^', '.', '#']]) == (2, 0)

def test_locate_guard_not_present():
    # Input: [['.', '#', '.'], ['.', '.', '#']]
    # Expected output: None since there is no guard present
    assert locate_guard([['.', '#', '.'], ['.', '.', '#']]) is None

def test_locate_guard_present_nonzero_column():
    # Input: [['.', '#', '.'], ['.', '^', '#'], ['.', '.', '#']]
    # Expected output: (1, 1) since the guard is at row 1, column 1
    assert locate_guard([['.', '#', '.'], ['.', '^', '#'], ['.', '.', '#']]) == (1, 1)

def test_trace_walk_with_guard():
    # Input: [['.', '#', '.'], ['^', '.', '#']]
    # The guard at (1, 0) will trace upwards to (0, 0)
    # Expected output: [['X', '#', '.'], ['X', '.', '#']]
    assert trace_walk([['.', '#', '.'], ['^', '.', '#']]) == [['X', '#', '.'], ['X', '.', '#']]

def test_trace_walk_with_guard_on_top_row():
    # Input: [['^', '#', '.'], ['.', '.', '#']]
    # The guard at (0, 0) will stay at its own cell
    # Expected output: [['X', '#', '.'], ['.', '.', '#']]
    assert trace_walk([['^', '#', '.'], ['.', '.', '#']]) == [['X', '#', '.'], ['.', '.', '#']]

def test_trace_walk_with_guard_upward_path_blocked():
    # Input: [['#', '#', '.'], ['^', '.', '.']]
    # The guard at (1, 0) cannot move up due to the obstruction
    # Expected output: [['#', '#', '.'], ['X', '.', '.']]
    assert trace_walk([['#', '#', '.'], ['^', '.', '.']]) == [['#', '#', '.'], ['X', '.', '.']]

def test_trace_walk_without_guard():
    # Input: [['.', '#', '.'], ['.', '.', '#']]
    # Expected output: [['.', '#', '.'], ['.', '.', '#']] since there is no guard
    assert trace_walk([['.', '#', '.'], ['.', '.', '#']]) == [['.', '#', '.'], ['.', '.', '#']]

def test_trace_walk_retains_input_grid():
    # Input: [['.', '#', '.'], ['^', '.', '#']]
    # The guard will trace upwards, but the input must remain unchanged
    input_grid = [['.', '#', '.'], ['^', '.', '#']]
    expected_output = [['X', '#', '.'], ['X', '.', '#']]
    assert trace_walk(input_grid) == expected_output
    assert input_grid == [['.', '#', '.'], ['^', '.', '#']]  # Ensure input grid is unchanged

def test_next_location_with_guard():
    # Input: [['.', '#', '.'], ['^', '.', '#']]
    # The guard at (1, 0) will next move to (0, 0)
    # Expected output: (0, 0)
    assert next_location([['.', '#', '.'], ['^', '.', '#']]) == (0, 0)

def test_next_location_with_guard_on_top_row():
    # Input: [['^', '#', '.'], ['.', '.', '#']]
    # The guard at (0, 0) will stay at its own cell
    # Expected output: (0, 0)
    assert next_location([['^', '#', '.'], ['.', '.', '#']]) == (0, 0)

def test_next_location_with_guard_in_nonzero_column():
    # Input: [['.', '.', '#'], ['.', '^', '#']]
    # The guard at (1, 1) will next move to (0, 1)
    # Expected output: (0, 1)
    assert next_location([['.', '.', '#'], ['.', '^', '#']]) == (0, 1)