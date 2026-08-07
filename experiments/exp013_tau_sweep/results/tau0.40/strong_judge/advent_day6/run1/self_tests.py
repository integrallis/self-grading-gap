from solution import parse_map, locate_guard, trace_guard_walk, next_guard_location

def test_parse_map():
    # AC-1.1: Each line of the input becomes one grid row
    input_map = "...\n#.#\n.#.\n"
    expected_output = [['.', '.', '.'], ['#', '.', '#'], ['.', '#', '.']]
    assert parse_map(input_map) == expected_output

    # AC-1.2: Rows are split on newlines only; every other character is kept as its own cell
    input_map = "# #\n. .\n"
    expected_output = [['#', ' ', '#'], ['.', ' ', '.']]
    assert parse_map(input_map) == expected_output

def test_locate_guard():
    # AC-2.1: Guard's position is reported as a row-and-column pair (top row case)
    input_map = "...\n.#.\n.^.\n"
    expected_output = (2, 1)  # Row 2, Column 1
    assert locate_guard(input_map) == expected_output

    # AC-2.1: Guard's position is reported as a row-and-column pair (top row case)
    input_map = "^..\n...\n...\n"
    expected_output = (0, 0)  # Row 0, Column 0
    assert locate_guard(input_map) == expected_output

    # AC-2.1: Guard's position is reported as a row-and-column pair (interior row case)
    input_map = "....\n..^.\n....\n"
    expected_output = (1, 2)  # Row 1, Column 2
    assert locate_guard(input_map) == expected_output

    # AC-2.2: When no guard appears on the grid, the position report is empty
    input_map = "...\n#.#\n.#.\n"
    expected_output = ""  # Representation for "empty" as per specification
    assert locate_guard(input_map) == expected_output

def test_trace_guard_walk():
    # AC-3.1: Guard walks straight up, marking cells with 'X'
    input_map = "...\n.#.\n.^.\n"
    expected_output = [['.', 'X', '.'], ['#', 'X', '#'], ['.', 'X', '.']]  # Guard moves from (2, 1) to (0, 1)
    assert trace_guard_walk(input_map) == expected_output

    # AC-3.1: Guard on top row
    input_map = "^..\n...\n...\n"
    expected_output = [['X', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]  # Only the starting cell marked
    assert trace_guard_walk(input_map) == expected_output

    # AC-3.1: Guard on bottom row of a two-row grid
    input_map = ".^.\n...\n"
    expected_output = [['X', '.', 'X'], ['.', '.', 'X']]  # Both cells in column 1 marked
    assert trace_guard_walk(input_map) == expected_output

    # AC-3.2: When the grid has no guard, the traced grid is identical to the input grid
    input_map = "...\n#.#\n.#.\n"
    expected_output = [['.', '.', '.'], ['#', '.', '#'], ['.', '#', '.']]
    assert trace_guard_walk(input_map) == expected_output

def test_next_guard_location():
    # AC-4.1: Next location of the guard given its row and column (top row case)
    input_map = "^..\n...\n...\n"
    expected_output = (0, 0)  # Row 0, Column 0
    assert next_guard_location(input_map) == expected_output

    # AC-4.1: Next location of the guard given its row and column (standard case)
    input_map = "...\n.#.\n.^.\n"
    expected_output = (1, 1)  # Row 1, Column 1
    assert next_guard_location(input_map) == expected_output

    # AC-4.1: Next location of the guard given its row and column (guard at column 2)
    input_map = "..^.\n....\n"
    expected_output = (0, 2)  # Row 0, Column 2
    assert next_guard_location(input_map) == expected_output