from solution import parse_map, locate_guard, trace_guard_walk, next_guard_location

def test_parse_map():
    # Test parsing a simple map into a grid
    input_map = "...\n#.#\n..."
    expected_output = [['.', '.', '.'], ['#', '.', '#'], ['.', '.', '.']]
    assert parse_map(input_map) == expected_output

def test_parse_map_with_spaces():
    # Test that spaces are treated as separate cells
    input_map = " . \n# #\n . "
    expected_output = [[' ', '.', ' '], ['#', ' ', '#'], [' ', '.', ' ']]
    assert parse_map(input_map) == expected_output

def test_locate_guard():
    # Test locating the guard's position when guard is on the top row
    input_map = "^..\n#.#\n..."
    expected_output = (0, 0)  # Guard is at row 0, column 0
    assert locate_guard(input_map) == expected_output

    # Test locating the guard's position when guard is in the middle row
    input_map = "...\n#^#\n..."
    expected_output = (1, 1)  # Guard is at row 1, column 1
    assert locate_guard(input_map) == expected_output

    # Test locating the guard's position when guard is on the bottom row
    input_map = "...\n#.#\n..^"
    expected_output = (2, 2)  # Guard is at row 2, column 2
    assert locate_guard(input_map) == expected_output

def test_locate_guard_no_guard():
    # Test when there is no guard on the map
    input_map = "...\n#.#\n..."
    expected_output = None  # No guard present
    assert locate_guard(input_map) == expected_output

def test_trace_guard_walk():
    # Test tracing the guard's walk starting from the middle row
    input_map = "...\n#^#\n..."
    expected_output = [['.', 'X', '.'], ['#', 'X', '#'], ['.', '.', '.']]
    assert trace_guard_walk(input_map) == expected_output

    # Test tracing the guard's walk when guard is on the top row
    input_map = "^..\n#.#\n..."
    expected_output = [['X', '.', '.'], ['#', '.', '#'], ['.', '.', '.']]
    assert trace_guard_walk(input_map) == expected_output

    # Test tracing the guard's walk when guard is on the bottom row in a two-row grid
    input_map = "...\n..^"
    expected_output = [['.', '.', 'X'], ['.', '.', 'X']]  # Guard moves up from (1,2) to (0,2)
    assert trace_guard_walk(input_map) == expected_output

def test_trace_guard_walk_with_obstruction():
    # Test tracing the guard's walk when guard is on the bottom row with obstruction
    input_map = "...\n#.#\n..^"
    expected_output = [['.', '.', 'X'], ['#', '.', 'X'], ['.', '.', 'X']]  # Guard moves up from (2,2) to (1,2) and (0,2)
    assert trace_guard_walk(input_map) == expected_output

def test_trace_guard_walk_no_guard():
    # Test tracing when there is no guard
    input_map = "...\n#.#\n..."
    expected_output = [['.', '.', '.'], ['#', '.', '#'], ['.', '.', '.']]
    assert trace_guard_walk(input_map) == expected_output

def test_next_guard_location():
    # Test getting the next location for the guard when guard is in the middle row
    input_map = "...\n#^#\n..."
    expected_output = (0, 1)  # Next location is row 0, column 1
    assert next_guard_location(input_map) == expected_output

    # Test next location when guard is on the top row at column 2
    input_map = "...\n#.#\n..^"
    expected_output = (1, 2)  # Next location is row 1, column 2
    assert next_guard_location(input_map) == expected_output

    # Test next location when guard is on the top row at column 2
    input_map = "^..\n#.#\n..."
    expected_output = (0, 2)  # Next location is row 0, column 2
    assert next_guard_location(input_map) == expected_output