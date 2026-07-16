# test_guard_patrol.py

from solution import parse_map, locate_guard, trace_guard_walk, report_next_location

def test_parse_map():
    # Input: 4 lines of a map
    input_map = "....\n#..#\n....\n#..#"
    # Expected output: grid representation of the map
    expected_output = [
        ['.', '.', '.', '.'],
        ['#', '.', '.', '#'],
        ['.', '.', '.', '.'],
        ['#', '.', '.', '#']
    ]
    assert parse_map(input_map) == expected_output

def test_locate_guard():
    # Input: map with a guard
    input_map = "....\n#^.#\n....\n#..#"
    # Expected output: position of the guard (1, 1)
    expected_output = (1, 1)
    assert locate_guard(input_map) == expected_output

    # Input: map without a guard
    input_map_no_guard = "....\n#.#.\n....\n#..#"
    # Expected output: empty when no guard is found
    expected_output_no_guard = ()
    assert locate_guard(input_map_no_guard) == expected_output_no_guard

def test_trace_guard_walk():
    # Input: map with a guard
    input_map_with_guard = "....\n#^.#\n....\n#..#"
    # Guard walks up from (1, 1) to (0, 1); expected output:
    expected_output = [
        ['.', 'X', '.', '.'],
        ['#', '.', '.', '#'],
        ['.', '.', '.', '.'],
        ['#', '.', '.', '#']
    ]
    assert trace_guard_walk(input_map_with_guard) == expected_output

    # Input: map without a guard
    input_map_no_guard = "....\n#.#.\n....\n#..#"
    # Expected output: same as input when no guard is found
    expected_output_no_guard = [
        ['.', '.', '.', '.'],
        ['#', '.', '#', '.'],
        ['.', '.', '.', '.'],
        ['#', '.', '.', '#']
    ]
    assert trace_guard_walk(input_map_no_guard) == expected_output_no_guard

def test_report_next_location():
    # Input: map with a guard
    input_map = "....\n#^.#\n....\n#..#"
    # Expected output: next location (0, 1)
    expected_output = (0, 1)
    assert report_next_location(input_map) == expected_output

    # Input: map without a guard
    input_map_no_guard = "....\n#.#.\n....\n#..#"
    # Expected output: empty when no guard is found
    expected_output_no_guard = ()
    assert report_next_location(input_map_no_guard) == expected_output_no_guard