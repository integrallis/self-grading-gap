import pytest

def test_create_field_with_given_width_and_height():
    field = create_field(3, 4)
    assert len(field) == 4  # Height: 4
    assert len(field[0]) == 3  # Width: 3

def test_field_with_no_mines_reports_zero_hints():
    field = create_field(2, 2)  # Create a 2x2 field
    for row in field:
        for cell in row:
            assert get_hint(cell) == 0  # AC-1.2: No mines should report 0

def test_mined_cell_reports_mine_marker():
    field = create_field(2, 2)
    field[0][0] = -1  # Place a mine at (0, 0)
    assert get_hint(field[0][0]) == -1  # AC-2.1: Mine marker is -1

def test_all_cells_mined_reports_mine_marker():
    field = create_field(2, 2)
    for row in field:
        for i in range(len(row)):
            row[i] = -1  # Place mines in all cells
    for row in field:
        for cell in row:
            assert get_hint(cell) == -1  # AC-2.2: Every cell reports -1

def test_safe_cell_reports_count_of_adjacent_mines():
    field = create_field(3, 3)
    field[0][0] = -1  # Place a mine at (0, 0)
    assert get_hint(field[0][1]) == 1  # AC-3.1: Adjacent to 1 mine
    assert get_hint(field[1][0]) == 1  # AC-3.1: Adjacent to 1 mine

def test_2_by_2_field_with_one_mine():
    field = create_field(2, 2)
    field[0][0] = -1  # Place a mine at (0, 0)
    assert get_hint(field[0][1]) == 1  # AC-3.2: 1 mine adjacent
    assert get_hint(field[1][0]) == 1  # AC-3.2: 1 mine adjacent
    assert get_hint(field[1][1]) == 1  # AC-3.2: 1 mine adjacent
    assert get_hint(field[0][0]) == -1  # Mine marker

def test_2_by_2_field_with_three_mines():
    field = create_field(2, 2)
    field[0][0] = -1  # Mine at (0, 0)
    field[0][1] = -1  # Mine at (0, 1)
    field[1][0] = -1  # Mine at (1, 0)
    assert get_hint(field[1][1]) == 3  # AC-3.2: 3 mines adjacent

def test_cell_with_no_adjacent_mines_reports_zero():
    field = create_field(3, 3)
    field[1][1] = -1  # Place a mine at (1, 1)
    assert get_hint(field[0][0]) == 1  # Adjacent to 1 mine
    assert get_hint(field[0][1]) == 1  # Adjacent to 1 mine
    assert get_hint(field[0][2]) == 1  # Adjacent to 1 mine
    assert get_hint(field[1][0]) == 1  # Adjacent to 1 mine
    assert get_hint(field[1][2]) == 1  # Adjacent to 1 mine
    assert get_hint(field[2][0]) == 1  # Adjacent to 1 mine
    assert get_hint(field[2][1]) == 1  # Adjacent to 1 mine
    assert get_hint(field[2][2]) == 1  # Adjacent to 1 mine

def test_3_by_3_example_with_mines():
    field = create_field(3, 3)
    field[0][0] = -1  # Place a mine at (0, 0)
    field[0][1] = -1  # Place a mine at (0, 1)
    assert get_hint(field[0][2]) == 1  # Top row: 1 mine adjacent
    assert get_hint(field[1][0]) == 2  # Middle row: 2 mines adjacent
    assert get_hint(field[1][1]) == 2  # Middle row: 2 mines adjacent
    assert get_hint(field[1][2]) == 1  # Middle row: 1 mine adjacent
    assert get_hint(field[2][0]) == 0  # Bottom row: 0 mines adjacent
    assert get_hint(field[2][1]) == 0  # Bottom row: 0 mines adjacent
    assert get_hint(field[2][2]) == 0  # Bottom row: 0 mines adjacent