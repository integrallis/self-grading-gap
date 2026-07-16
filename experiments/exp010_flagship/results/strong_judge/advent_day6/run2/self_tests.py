from solution import parse_map, locate_guard, trace_guard_walk, next_guard_location

def test_parse_map():
    # Input map has 4 lines, each character becomes a grid cell
    input_map = "...\n.#.\n...\n..."
    expected_output = [
        ['.', '.', '.'],
        ['.', '#', '.'],
        ['.', '.', '.'],
        ['.', '.', '.']
    ]
    assert parse_map(input_map) == expected_output

def test_parse_map_with_spaces():
    # Input map includes spaces, which should be preserved as cells
    input_map = ". .\n# ^"
    expected_output = [
        ['.', ' '],
        ['#', ' ']
    ]
    assert parse_map(input_map) == expected_output

def test_parse_map_with_tabs():
    # Input map includes tabs, which should be preserved as cells
    input_map = ".\t.\n#\t^"
    expected_output = [
        ['.', '\t', '.'],
        ['#', '\t', '^']
    ]
    assert parse_map(input_map) == expected_output

def test_locate_guard_found():
    # Guard at row 1, column 1
    input_map = "...\n.^.\n..."
    expected_output = (1, 1)  # row 1, column 1
    assert locate_guard(input_map) == expected_output

def test_locate_guard_on_top_row():
    # Guard at the top row
    input_map = "^\n.\n."
    expected_output = (0, 0)  # row 0, column 0
    assert locate_guard(input_map) == expected_output

def test_locate_guard_on_bottom_row():
    # Guard at the bottom row
    input_map = ".\n^"
    expected_output = (1, 0)  # row 1, column 0
    assert locate_guard(input_map) == expected_output

def test_locate_guard_not_found():
    # No guard in the map
    input_map = "...\n.#.\n..."
    expected_output = ()  # no guard present, unspecified representation
    assert locate_guard(input_map) == expected_output

def test_trace_guard_walk():
    # Guard at row 1, column 1, walks up to row 0
    input_map = "...\n.^.\n..."
    expected_output = [
        ['.', 'X', '.'],
        ['.', 'X', '.'],
        ['.', '.', '.']
    ]
    assert trace_guard_walk(input_map) == expected_output

def test_trace_guard_walk_guard_on_top():
    # Guard at the top row
    input_map = "^\n.\n."
    expected_output = [
        ['X'],
        ['.'],
        ['.']
    ]
    assert trace_guard_walk(input_map) == expected_output

def test_trace_guard_walk_guard_on_bottom():
    # Guard at the bottom row of a two-row grid
    input_map = ".\n^"
    expected_output = [
        ['X'],
        ['X']
    ]
    assert trace_guard_walk(input_map) == expected_output

def test_trace_guard_walk_no_guard():
    # No guard, grid remains the same
    input_map = "...\n.#.\n..."
    expected_output = [
        ['.', '.', '.'],
        ['.', '#', '.'],
        ['.', '.', '.']
    ]
    assert trace_guard_walk(input_map) == expected_output

def test_next_guard_location():
    # Guard at row 1, column 1, next location is row 0, column 1
    input_map = "...\n.^.\n..."
    expected_output = (0, 1)  # row 0, column 1
    assert next_guard_location(input_map) == expected_output

def test_next_guard_location_guard_on_top():
    # Guard at row 0, column 2, next location is row 0, column 2
    input_map = "..^\n..."
    expected_output = (0, 2)  # row 0, column 2
    assert next_guard_location(input_map) == expected_output