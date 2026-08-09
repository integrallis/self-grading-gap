# your complete test file
import pytest
from solution import create_field, get_cell_hint

def test_create_field_with_given_dimensions():
    field = create_field(3, 2)  # 3 columns, 2 rows
    # No specific verification of dimensions, as the representation is not defined.

def test_field_with_no_mines_reports_zero_hints():
    field = create_field(2, 2)  # 2x2 field
    hints = [get_cell_hint(field, x, y) for x in range(2) for y in range(2)]
    assert all(hint == 0 for hint in hints)  # all cells should report 0

def test_cell_with_mine_reports_mine_marker():
    field = create_field(2, 2)
    field[0][0] = -1  # Place a mine at (0, 0)
    hint = get_cell_hint(field, 0, 0)
    assert hint == -1  # cell with mine should report -1

def test_all_cells_mined_reports_mine_marker():
    field = create_field(2, 2)
    for x in range(2):
        for y in range(2):
            field[y][x] = -1  # Place mines in all cells
    hints = [get_cell_hint(field, x, y) for x in range(2) for y in range(2)]
    assert all(hint == -1 for hint in hints)  # all cells should report -1

def test_safe_cell_reports_count_of_adjacent_mines():
    field = create_field(3, 3)
    field[0][0] = -1  # Place mine at (0, 0)
    field[0][1] = -1  # Place mine at (0, 1)
    hint = get_cell_hint(field, 1, 0)  # (1, 0) should count adjacent mines
    assert hint == 1  # (1, 0) has 1 adjacent mine

def test_cell_with_no_adjacent_mines_reports_zero():
    field = create_field(3, 3)
    field[2][2] = -1  # Place a mine at (2, 2)
    hint = get_cell_hint(field, 0, 0)  # (0, 0) is safe and has no adjacent mines
    assert hint == 0  # should report 0

def test_2_by_2_field_counts_adjacent_mines_correctly():
    field = create_field(2, 2)
    field[0][0] = -1  # Place mine at (0, 0)
    field[0][1] = -1  # Place mine at (0, 1)
    hints = [get_cell_hint(field, x, y) for x in range(2) for y in range(2)]
    assert hints == [-1, -1, 2, 2]  # cells should report as per adjacent mines

def test_three_by_three_field_example():
    field = create_field(3, 3)
    field[0][0] = -1  # Place mine at (0, 0)
    field[0][1] = -1  # Place mine at (0, 1)
    hints = [get_cell_hint(field, x, y) for y in range(3) for x in range(3)]
    expected_hints = [-1, -1, 1, 2, 2, 1, 0, 0, 0]  # Expected hints based on mine placements
    assert hints == expected_hints  # Check if hints match expected values

def test_2_by_2_field_with_one_mine():
    field = create_field(2, 2)
    field[0][0] = -1  # Place mine at (0, 0)
    hints = [get_cell_hint(field, x, y) for x in range(2) for y in range(2)]
    assert hints == [-1, 1, 1, 1]  # One mine, safe cells should report 1

def test_2_by_2_field_with_three_mines():
    field = create_field(2, 2)
    field[0][0] = -1  # Place mine at (0, 0)
    field[0][1] = -1  # Place mine at (0, 1)
    field[1][0] = -1  # Place mine at (1, 0)
    hints = [get_cell_hint(field, x, y) for x in range(2) for y in range(2)]
    assert hints == [-1, -1, -1, 3]  # Three mines, safe cell should report 3

def test_diagonal_mine_contributes_to_hint():
    field = create_field(3, 3)
    field[0][0] = -1  # Place mine at (0, 0)
    hint = get_cell_hint(field, 1, 1)  # (1, 1) should count diagonal mine
    assert hint == 1  # Should report 1 due to the diagonal mine