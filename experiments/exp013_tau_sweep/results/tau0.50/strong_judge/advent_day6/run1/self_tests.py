# test_guard_patrol.py

from solution import parse_map, locate_guard, trace_guard_walk, report_next_location

def test_parse_map_single_line():
    # Input: a single line "..."
    # Expected output: [['.', '.', '.']]
    assert parse_map("...") == [['.', '.', '.']]

def test_parse_map_multiple_lines():
    # Input: a four-line map of dots and hash marks
    # Expected output: [['.', '#', '.'],
    #                   ['.', '.', '.'],
    #                   ['#', '.', '#'],
    #                   ['.', '#', '.']]
    assert parse_map(".#.\n...\n#.#\n.#.") == [['.', '#', '.'], 
                                               ['.', '.', '.'], 
                                               ['#', '.', '#'], 
                                               ['.', '#', '.']]

def test_parse_map_spaces_and_other_chars():
    # Input: a grid with spaces and other characters
    # Expected output: [['.', ' ', '.'], 
    #                   ['#', ' ', '#']]
    assert parse_map(". .\n# #") == [['.', ' ', '.'], ['#', ' ', '#']]

def test_parse_map_split_on_newlines_only():
    # Input: a grid with \r and \n
    # Expected output: [['.', '\r'], ['#']]
    assert parse_map(".\r\n#") == [['.', '\r'], ['#']]

def test_locate_guard_present():
    # Input: a grid with a guard at (1, 1)
    # Expected output: (1, 1)
    assert locate_guard([['.', '#', '.'], 
                         ['.', '^', '.'], 
                         ['#', '.', '#']]) == (1, 1)

def test_locate_guard_top_row():
    # Input: a grid with a guard at the top row (0, 2)
    # Expected output: (0, 2)
    assert locate_guard([['.', '#', '^'], 
                         ['.', '.', '.'], 
                         ['#', '.', '#']]) == (0, 2)

def test_locate_guard_bottom_row():
    # Input: a grid with a guard at the bottom row (2, 1)
    # Expected output: (2, 1)
    assert locate_guard([['.', '#', '.'], 
                         ['.', '.', '.'], 
                         ['#', '^', '#']]) == (2, 1)

def test_locate_guard_not_present():
    # Input: a grid without a guard
    # Expected output: empty (not specified what this is)
    assert locate_guard([['.', '#', '.'], 
                         ['.', '.', '.'], 
                         ['#', '.', '#']]) == []  # Assuming empty representation is an empty list

def test_trace_guard_walk():
    # Input: a guard on row 1, column 1
    # Expected output: [['.', 'X', '.'], 
    #                   ['.', 'X', '.'], 
    #                   ['#', '.', '#']]
    assert trace_guard_walk([['.', '#', '.'], 
                              ['.', '^', '.'], 
                              ['#', '.', '#']]) == [['.', 'X', '.'], 
                                                     ['.', 'X', '.'], 
                                                     ['#', '.', '#']]

def test_trace_guard_walk_top_row():
    # Input: a guard on top row (0, 2)
    # Expected output: [['.', '.', 'X']]
    assert trace_guard_walk([['.', '.', '^']]) == [['.', '.', 'X']]

def test_trace_guard_walk_bottom_row():
    # Input: a guard on bottom row (2, 1)
    # Expected output: [['.', 'X', '.'], 
    #                   ['.', 'X', '.'], 
    #                   ['#', '.', '#']]
    assert trace_guard_walk([['.', '#', '.'], 
                              ['.', 'X', '.'], 
                              ['#', '^', '#']]) == [['.', 'X', '.'], 
                                                     ['.', 'X', '.'], 
                                                     ['#', '.', '#']]

def test_trace_guard_walk_no_guard():
    # Input: a grid without a guard
    # Expected output: identical to input
    input_grid = [['.', '#', '.'], 
                   ['.', '.', '.'], 
                   ['#', '.', '#']]
    output_grid = trace_guard_walk(input_grid)
    assert output_grid == input_grid  # check content equality
    assert output_grid is not input_grid  # ensure it's a copy

def test_report_next_location():
    # Input: guard at (1, 1)
    # Expected output: (0, 1)
    assert report_next_location([['.', '#', '.'], 
                                  ['.', '^', '.'], 
                                  ['#', '.', '#']]) == (0, 1)

def test_report_next_location_guard_on_top_row():
    # Input: guard at (0, 2)
    # Expected output: (0, 2)
    assert report_next_location([['.', '#', '^'], 
                                  ['.', '.', '.'], 
                                  ['#', '.', '#']]) == (0, 2)