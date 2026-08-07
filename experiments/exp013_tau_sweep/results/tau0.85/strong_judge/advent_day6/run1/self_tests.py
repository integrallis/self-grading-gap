# test_guard_patrol.py

from solution import parse_map, locate_guard, trace_guard_walk, next_guard_location

def test_parse_map():
    # Testing a simple map
    input_map = "...\n#.#\n..."
    expected_output = [['.', '.', '.'], ['#', '.', '#'], ['.', '.', '.']]
    assert parse_map(input_map) == expected_output

    # Testing a map with spaces
    input_map = " . \n# #\n . "
    expected_output = [[' ', '.', ' '], ['#', ' ', '#'], [' ', '.', ' ']]
    assert parse_map(input_map) == expected_output

    # Testing with non-newline line separator
    input_map = "a\vb"
    expected_output = [['a', '\v', 'b']]  # Only \n should create rows
    assert parse_map(input_map) == expected_output

def test_locate_guard():
    # Testing map with a guard present
    input_map = "...\n#^#\n..."
    expected_output = (1, 1)  # Row 1, Column 1
    assert locate_guard(input_map) == expected_output

    # Testing map with a guard at the top
    input_map = "^..\n#.#\n..."
    expected_output = (0, 0)  # Row 0, Column 0
    assert locate_guard(input_map) == expected_output

    # Testing map with a guard at the bottom
    input_map = "...\n#.#\n..^"
    expected_output = (2, 2)  # Row 2, Column 2
    assert locate_guard(input_map) == expected_output

    # Testing map without a guard
    input_map = "...\n#.#\n..."
    expected_output = ()  # No guard present
    assert locate_guard(input_map) == expected_output

def test_trace_guard_walk():
    # Testing tracing with guard in the middle
    input_map = "...\n#^#\n..."
    expected_output = [['.', 'X', '.'], ['#', 'X', '#'], ['.', '.', '.']]
    assert trace_guard_walk(input_map) == expected_output

    # Testing tracing with guard at the top
    input_map = "^..\n#.#\n..."
    expected_output = [['X', '.', '.'], ['#', '.', '#'], ['.', '.', '.']]
    assert trace_guard_walk(input_map) == expected_output

    # Testing tracing with guard at the bottom
    input_map = "...\n#.#\n..^"
    expected_output = [['.', '.', 'X'], ['#', '.', 'X'], ['.', '.', 'X']]
    assert trace_guard_walk(input_map) == expected_output

    # Testing tracing with no guard
    input_map = "...\n#.#\n..."
    expected_output = [['.', '.', '.'], ['#', '.', '#'], ['.', '.', '.']]
    assert trace_guard_walk(input_map) == expected_output

def test_next_guard_location():
    # Testing with guard at the top
    input_map = "^..\n#.#\n..."
    expected_output = (0, 0)  # Row 0, Column 0
    assert next_guard_location(input_map) == expected_output

    # Testing with guard in the middle
    input_map = "...\n#^#\n..."
    expected_output = (0, 1)  # Row 0, Column 1
    assert next_guard_location(input_map) == expected_output

    # Testing with guard at the bottom
    input_map = "...\n#.#\n..^"
    expected_output = (1, 2)  # Row 1, Column 2
    assert next_guard_location(input_map) == expected_output

    # Testing with no guard (no specification for next location behavior)
    input_map = "...\n#.#\n..."
    # Not asserting anything for this case as per the current specification