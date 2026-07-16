# test_minesweeper.py

from solution import create_field, get_hint

def test_create_field_with_given_dimensions():
    field = create_field(3, 2)  # Create a 3x2 field
    assert len(field) == 2  # Check the number of rows
    assert len(field[0]) == 3  # Check the number of columns
    assert len(field[1]) == 3  # Check the number of columns in the second row

def test_empty_field_reports_zero_hints():
    field = create_field(3, 2)  # Create a 3x2 field
    for row in range(2):
        for col in range(3):
            assert get_hint(field, col, row) == 0  # All cells should report 0

def test_mined_cell_reports_mine_marker():
    field = create_field(3, 2)  # Create a 3x2 field
    field[0][0] = -1  # Place a mine at (0, 0)
    assert get_hint(field, 0, 0) == -1  # The mined cell should report -1

def test_all_cells_mined_reports_mine_marker():
    field = create_field(2, 2)  # Create a 2x2 field
    for row in range(2):
        for col in range(2):
            field[row][col] = -1  # Mine every cell
    for row in range(2):
        for col in range(2):
            assert get_hint(field, col, row) == -1  # All cells should report -1

def test_safe_cell_counts_adjacent_mines():
    field = create_field(3, 3)  # Create a 3x3 field
    field[0][0] = -1  # Place a mine at (0, 0)
    field[0][1] = -1  # Place a mine at (0, 1)
    assert get_hint(field, 0, 0) == -1  # (0, 0) is a mine
    assert get_hint(field, 0, 1) == -1  # (0, 1) is a mine
    assert get_hint(field, 0, 2) == 1  # (0, 2) has 1 mine adjacent
    assert get_hint(field, 1, 0) == -1  # (1, 0) is a mine
    assert get_hint(field, 1, 1) == 2  # (1, 1) has 2 mines adjacent
    assert get_hint(field, 1, 2) == 1  # (1, 2) has 1 mine adjacent
    assert get_hint(field, 2, 0) == 0  # (2, 0) has 0 mines adjacent
    assert get_hint(field, 2, 1) == 0  # (2, 1) has 0 mines adjacent
    assert get_hint(field, 2, 2) == 0  # (2, 2) has 0 mines adjacent

def test_2_by_2_field_with_mines():
    field = create_field(2, 2)  # Create a 2x2 field
    field[0][0] = -1  # Place a mine at (0, 0)
    assert get_hint(field, 0, 0) == -1  # (0, 0) is a mine
    assert get_hint(field, 0, 1) == 1  # (0, 1) has 1 mine adjacent
    assert get_hint(field, 1, 0) == 1  # (1, 0) has 1 mine adjacent
    assert get_hint(field, 1, 1) == 2  # (1, 1) has 2 mines adjacent

def test_2_by_2_field_with_two_mines():
    field = create_field(2, 2)  # Create a 2x2 field
    field[0][0] = -1  # Place a mine at (0, 0)
    field[0][1] = -1  # Place a mine at (0, 1)
    assert get_hint(field, 1, 0) == 2  # (1, 0) has 2 mines adjacent
    assert get_hint(field, 1, 1) == 2  # (1, 1) has 2 mines adjacent

def test_2_by_2_field_with_three_mines():
    field = create_field(2, 2)  # Create a 2x2 field
    field[0][0] = -1  # Place a mine at (0, 0)
    field[0][1] = -1  # Place a mine at (0, 1)
    field[1][0] = -1  # Place a mine at (1, 0)
    assert get_hint(field, 1, 1) == 3  # (1, 1) has 3 mines adjacent

def test_cell_with_no_adjacent_mines_reports_zero():
    field = create_field(3, 3)  # Create a 3x3 field
    field[0][0] = -1  # Place a mine at (0, 0)
    assert get_hint(field, 2, 2) == 0  # (2, 2) has 0 adjacent mines

def test_worked_3_by_3_example():
    field = create_field(3, 3)  # Create a 3x3 field
    field[0][0] = -1  # Place a mine at (0, 0)
    field[1][0] = -1  # Place a mine at (1, 0)
    assert get_hint(field, 0, 0) == -1  # (0, 0) is a mine
    assert get_hint(field, 1, 0) == -1  # (1, 0) is a mine
    assert get_hint(field, 0, 1) == 1  # (0, 1) has 1 mine adjacent
    assert get_hint(field, 0, 2) == 2  # (0, 2) has 2 mines adjacent
    assert get_hint(field, 1, 1) == 2  # (1, 1) has 2 mines adjacent
    assert get_hint(field, 1, 2) == 1  # (1, 2) has 1 mine adjacent
    assert get_hint(field, 2, 0) == 0  # (2, 0) has 0 mines adjacent
    assert get_hint(field, 2, 1) == 0  # (2, 1) has 0 mines adjacent
    assert get_hint(field, 2, 2) == 0  # (2, 2) has 0 mines adjacent

def test_coordinate_orientation():
    field = create_field(2, 3)  # Create a non-square 2x3 field
    assert len(field) == 2  # Check the number of rows
    assert len(field[0]) == 3  # Check the number of columns
    assert len(field[1]) == 3  # Check the number of columns in the second row