import pytest
from solution import create_field, get_cell_hint

def test_create_field_with_given_dimensions():
    field = create_field(3, 2)
    # The field should have 2 rows (height) and 3 columns (width)
    assert len(field) == 2  # height = 2 rows
    assert len(field[0]) == 3  # width = 3 columns
    assert len(field[1]) == 3  # width = 3 columns

def test_field_with_no_mines_reports_zero_hints():
    field = create_field(3, 2)
    for row in range(2):  # 2 rows
        for col in range(3):  # 3 columns
            assert get_cell_hint(field, col, row) == 0  # No mines, so hint is 0

def test_mined_cell_reports_mine_marker():
    field = create_field(3, 2)
    field[0][0] = -1  # Place a mine at (0, 0)
    assert get_cell_hint(field, 0, 0) == -1  # Mined cell reports -1

def test_field_with_all_mined_cells_reports_mine_marker():
    field = create_field(2, 2)
    field[0][0] = -1
    field[0][1] = -1
    field[1][0] = -1
    field[1][1] = -1
    for row in range(2):
        for col in range(2):
            assert get_cell_hint(field, col, row) == -1  # All cells report -1

def test_safe_cell_reports_number_of_adjacent_mines():
    field = create_field(3, 3)
    field[0][0] = -1  # Mine at (0, 0)
    assert get_cell_hint(field, 0, 1) == 2  # (0, 1) has 2 mines around
    assert get_cell_hint(field, 1, 0) == 1  # (1, 0) has 1 mine around
    assert get_cell_hint(field, 1, 1) == 1  # (1, 1) has 1 mine around
    assert get_cell_hint(field, 0, 2) == 0  # (0, 2) has no adjacent mines
    assert get_cell_hint(field, 2, 2) == 0  # (2, 2) has no adjacent mines

def test_2_by_2_field_with_one_mine_reports_correct_hints():
    field = create_field(2, 2)
    field[0][0] = -1  # Mine at (0, 0)
    assert get_cell_hint(field, 0, 1) == 1  # (0, 1) has 1 mine around
    assert get_cell_hint(field, 1, 0) == 1  # (1, 0) has 1 mine around
    assert get_cell_hint(field, 1, 1) == 1  # (1, 1) has 1 mine around
    assert get_cell_hint(field, 0, 0) == -1  # (0, 0) is a mine

def test_2_by_2_field_with_two_mines_reports_correct_hints():
    field = create_field(2, 2)
    field[0][0] = -1  # Mine at (0, 0)
    field[0][1] = -1  # Mine at (0, 1)
    assert get_cell_hint(field, 1, 0) == 2  # (1, 0) has 2 mines around
    assert get_cell_hint(field, 1, 1) == 2  # (1, 1) has 2 mines around
    assert get_cell_hint(field, 0, 0) == -1  # (0, 0) is a mine
    assert get_cell_hint(field, 0, 1) == -1  # (0, 1) is a mine

def test_2_by_2_field_with_three_mines_reports_correct_hints():
    field = create_field(2, 2)
    field[0][0] = -1  # Mine at (0, 0)
    field[0][1] = -1  # Mine at (0, 1)
    field[1][0] = -1  # Mine at (1, 0)
    assert get_cell_hint(field, 1, 1) == 3  # (1, 1) has 3 mines around
    assert get_cell_hint(field, 0, 0) == -1  # (0, 0) is a mine
    assert get_cell_hint(field, 0, 1) == -1  # (0, 1) is a mine
    assert get_cell_hint(field, 1, 0) == -1  # (1, 0) is a mine

def test_3_by_3_field_example():
    field = create_field(3, 3)
    field[0][0] = -1  # Mine at (0, 0)
    field[0][1] = -1  # Mine at (0, 1)
    assert get_cell_hint(field, 0, 1) == 2  # (0, 1) has 2 mines around
    assert get_cell_hint(field, 1, 0) == -1  # (1, 0) is a mine
    assert get_cell_hint(field, 1, 1) == 2  # (1, 1) has 2 mines around
    assert get_cell_hint(field, 1, 2) == 1  # (1, 2) has 1 mine around
    assert get_cell_hint(field, 0, 2) == 0  # (0, 2) has no adjacent mines
    assert get_cell_hint(field, 2, 0) == 1  # (2, 0) has 1 mine around
    assert get_cell_hint(field, 2, 1) == 1  # (2, 1) has 1 mine around
    assert get_cell_hint(field, 2, 2) == 0  # (2, 2) has no adjacent mines