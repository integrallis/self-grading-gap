# test_guard_patrol.py

from solution import parse_map, locate_guard, trace_guard_walk, report_next_location

def test_parse_map():
    # Test parsing a four-line map
    input_map = "...\n.#.\n...\n..."
    expected_output = [['.', '.', '.'], ['.', '#', '.'], ['.', '.', '.'], ['.', '.', '.']]  # 4 rows, 3 columns
    assert parse_map(input_map) == expected_output

    # Test parsing a map with spaces
    input_map = " . . \n# # #\n . . "
    expected_output = [[' ', '.', ' ', '.', ' '], ['#', ' ', '#', ' ', '#'], [' ', '.', ' ', '.', ' ']]
    assert parse_map(input_map) == expected_output  # 3 rows, 5 columns

    # Test parsing a single line map
    input_map = "..."
    expected_output = [['.', '.', '.']]
    assert parse_map(input_map) == expected_output  # 1 row, 3 columns

def test_locate_guard():
    # Test locating guard at the top row
    input_map = "^..\n.#.\n..."
    expected_output = (0, 0)  # Guard at row 0, column 0
    assert locate_guard(parse_map(input_map)) == expected_output

    # Test locating guard at the bottom row
    input_map = "...\n.#.\n..^"
    expected_output = (2, 2)  # Guard at row 2, column 2
    assert locate_guard(parse_map(input_map)) == expected_output

    # Test when there is no guard
    input_map = "...\n.#.\n..."
    expected_output = ()  # No guard present
    assert locate_guard(parse_map(input_map)) == expected_output

    # Test locating guard in a middle row
    input_map = "...\n.^.\n..."
    expected_output = (1, 1)  # Guard at row 1, column 1
    assert locate_guard(parse_map(input_map)) == expected_output

def test_trace_guard_walk():
    # Test tracing guard walk with no guard
    input_map = "...\n.#.\n..."
    expected_output = [['.', '.', '.'], ['.', '#', '.'], ['.', '.', '.']]  # No guard, identical map
    assert trace_guard_walk(parse_map(input_map)) == expected_output

    # Test tracing guard walk with guard at the top row
    input_map = "^..\n.#.\n..."
    expected_output = [['X', '.', '.'], ['.', '#', '.'], ['.', '.', '.']]  # Guard at top
    assert trace_guard_walk(parse_map(input_map)) == expected_output

    # Test tracing guard walk with guard at the bottom row
    input_map = "...\n.#.\n..^"
    expected_output = [['.', '.', 'X'], ['.', '#', 'X'], ['.', '.', 'X']]  # Guard marks all cells above
    assert trace_guard_walk(parse_map(input_map)) == expected_output

    # Test tracing guard walk on a two-row grid with guard in the bottom row
    input_map = "...\n..^"
    expected_output = [['.', '.', 'X'], ['.', '.', 'X']]  # Guard marks both cells in its column
    assert trace_guard_walk(parse_map(input_map)) == expected_output

def test_report_next_location():
    # Test reporting next location with guard present at top row
    input_map = "^..\n.#.\n..."
    expected_output = (0, 0)  # Next location is row 0, column 0
    assert report_next_location(parse_map(input_map)) == expected_output

    # Test reporting next location with guard in the middle row
    input_map = "...\n.^.\n..."
    expected_output = (0, 1)  # Next location is row 0, column 1
    assert report_next_location(parse_map(input_map)) == expected_output

    # Test reporting next location with no guard
    input_map = "...\n.#.\n..."
    expected_output = ()  # No guard to report next location
    assert report_next_location(parse_map(input_map)) == expected_output