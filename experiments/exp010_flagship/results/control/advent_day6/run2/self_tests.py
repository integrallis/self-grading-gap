# test_guard_patrol.py

from solution import parse_map, locate_guard, trace_walk, next_location

def test_parse_map():
    # Given a raw map text with 4 lines
    raw_map = "....\n....\n....\n...."
    # It should be converted into a 4x4 grid of characters
    expected_grid = [['.', '.', '.', '.'],
                     ['.', '.', '.', '.'],
                     ['.', '.', '.', '.'],
                     ['.', '.', '.', '.']]
    assert parse_map(raw_map) == expected_grid

def test_parse_map_with_obstructions():
    # Given a raw map text with obstructions
    raw_map = "#..#\n....\n#..#"
    # The grid should contain the correct characters
    expected_grid = [['#', '.', '.', '#'],
                     ['.', '.', '.', '.'],
                     ['#', '.', '.', '#']]
    assert parse_map(raw_map) == expected_grid

def test_locate_guard():
    # Given a grid with a guard
    grid = [['.', '.', '^', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.']]
    # The guard's position should be reported as (0, 2)
    assert locate_guard(grid) == (0, 2)

def test_locate_guard_not_found():
    # Given a grid without a guard
    grid = [['.', '.', '.', '.'],
            ['.', '.', '.', '.']]
    # The position report should be empty
    assert locate_guard(grid) == None

def test_trace_walk():
    # Given a grid with a guard at (2, 1)
    grid = [['.', '.', '.'],
            ['.', '^', '.'],
            ['.', '.', '.']]
    # The guard will trace its walk to the top row, marking cells with 'X'
    expected_grid = [['.', 'X', '.'],
                     ['.', 'X', '.'],
                     ['.', '.', '.']]
    assert trace_walk(grid) == expected_grid

def test_trace_walk_guard_on_top_row():
    # Given a grid with a guard on the top row
    grid = [['^', '.', '.'],
            ['.', '.', '.']]
    # The guard's walk should only mark the starting cell
    expected_grid = [['X', '.', '.'],
                     ['.', '.', '.']]
    assert trace_walk(grid) == expected_grid

def test_trace_walk_guard_not_found():
    # Given a grid without a guard
    grid = [['.', '.', '.'],
            ['.', '.', '.']]
    # The traced grid should be identical to the input grid
    assert trace_walk(grid) == grid

def test_next_location():
    # Given a grid with a guard at (1, 1)
    grid = [['.', '.', '.'],
            ['.', '^', '.'],
            ['.', '.', '.']]
    # The next location of the guard should be reported as (0, 1)
    assert next_location(grid) == (0, 1)

def test_next_location_guard_on_top_row():
    # Given a guard on the top row
    grid = [['^', '.', '.'],
            ['.', '.', '.']]
    # The next location should still be (0, 0)
    assert next_location(grid) == (0, 0)

def test_next_location_guard_not_found():
    # Given a grid without a guard
    grid = [['.', '.', '.'],
            ['.', '.', '.']]
    # The next location should be None
    assert next_location(grid) == None