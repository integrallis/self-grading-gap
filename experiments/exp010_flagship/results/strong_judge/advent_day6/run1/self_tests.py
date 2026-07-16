# your complete test file
import pytest
from solution import parse_map, locate_guard, trace_guard_walk, report_next_location

def test_parse_map_single_line():
    input_map = ".#."
    expected_output = [['.', '#', '.']]  # Each character becomes a single cell
    assert parse_map(input_map) == expected_output

def test_parse_map_multiple_lines():
    input_map = ".#.\n.#."
    expected_output = [['.', '#', '.'], ['.', '#', '.']]  # Two rows from two lines
    assert parse_map(input_map) == expected_output

def test_parse_map_with_spaces():
    input_map = ". # .\n # \n.#."
    expected_output = [['.', ' ', '#', ' ', '.'], [' ', '#', ' '], ['.', '#', '.']]  # Spaces are kept as cells
    assert parse_map(input_map) == expected_output

def test_locate_guard_present_top():
    input_grid = [['^', '.', '.'], ['.', '.', '.']]
    expected_output = (0, 0)  # Guard at (0, 0)
    assert locate_guard(input_grid) == expected_output

def test_locate_guard_present_middle():
    input_grid = [['.', '.', '.'], ['^', '.', '.']]
    expected_output = (1, 0)  # Guard at (1, 0)
    assert locate_guard(input_grid) == expected_output

def test_locate_guard_present_bottom():
    input_grid = [['.', '.', '.'], ['.', '.', '^']]
    expected_output = (1, 2)  # Guard at (1, 2)
    assert locate_guard(input_grid) == expected_output

def test_locate_guard_absent():
    input_grid = [['.', '#', '.'], ['#', '#', '.']]
    expected_output = ()  # No guard present
    assert locate_guard(input_grid) == expected_output

def test_trace_guard_walk_from_top():
    input_grid = [['^', '.', '.'], ['.', '.', '.']]
    expected_output = [['X', '.', '.'], ['.', '.', '.']]  # Guard is at the top, marks only its cell
    assert trace_guard_walk(input_grid) == expected_output

def test_trace_guard_walk_from_middle():
    input_grid = [['.', '.', '.'], ['^', '.', '.']]
    expected_output = [['X', '.', '.'], ['X', '.', '.']]  # Guard walks up, marking 'X'
    assert trace_guard_walk(input_grid) == expected_output

def test_trace_guard_walk_from_bottom():
    input_grid = [['.', '.', '.'], ['.', '.', '^']]
    expected_output = [['.', '.', 'X'], ['.', '.', 'X']]  # Guard at bottom, marks column
    assert trace_guard_walk(input_grid) == expected_output

def test_trace_guard_walk_no_guard():
    input_grid = [['.', '#', '.'], ['#', '#', '.']]
    expected_output = [['.', '#', '.'], ['#', '#', '.']]  # No guard, grid unchanged
    assert trace_guard_walk(input_grid) == expected_output

def test_report_next_location_top():
    input_grid = [['^', '.', '.'], ['.', '.', '.']]
    expected_output = (0, 0)  # Next location is the guard's current position
    assert report_next_location(input_grid) == expected_output

def test_report_next_location_middle():
    input_grid = [['.', '.', '.'], ['^', '.', '.']]
    expected_output = (0, 0)  # Next location is directly above the guard
    assert report_next_location(input_grid) == expected_output

def test_report_next_location_bottom():
    input_grid = [['.', '.', '.'], ['.', '.', '^']]
    expected_output = (0, 2)  # Next location is directly above the guard
    assert report_next_location(input_grid) == expected_output

def test_report_next_location_from_third_row():
    input_grid = [['.', '.', '.'], ['.', '^', '.'], ['.', '.', '.']]
    expected_output = (0, 1)  # Next location is directly above the guard
    assert report_next_location(input_grid) == expected_output

def test_trace_guard_walk_copy():
    input_grid = [['.', '.', '.'], ['^', '.', '.']]
    traced_grid = trace_guard_walk(input_grid)
    expected_output = [['X', '.', '.'], ['X', '.', '.']]  # Guard walks up, marking 'X'
    assert traced_grid == expected_output
    assert input_grid == [['.', '.', '.'], ['^', '.', '.']]  # Original grid unchanged