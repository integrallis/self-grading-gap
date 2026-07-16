import pytest
from solution import create_field, get_hint

def test_create_field_with_no_mines():
    field = create_field(3, 3)  # A 3x3 field
    assert field == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # All cells report 0

def test_create_field_with_mines():
    field = create_field(3, 3)
    field[0][0] = -1  # Place a mine
    assert field[0][0] == -1  # The mined cell should report the mine marker

def test_get_hint_for_mined_cell():
    field = create_field(3, 3)
    field[1][1] = -1  # Place a mine at (1, 1)
    assert get_hint(field, 1, 1) == -1  # Mined cell should return -1

def test_get_hint_for_empty_cell_with_no_adjacent_mines():
    field = create_field(3, 3)
    assert get_hint(field, 0, 0) == 0  # No adjacent mines, should return 0

def test_get_hint_for_empty_cell_with_adjacent_mines():
    field = create_field(3, 3)
    field[1][1] = -1  # Place a mine at (1, 1)
    assert get_hint(field, 0, 0) == 0  # Cell (0, 0) has no adjacent mines

def test_get_hint_for_all_mined_cells():
    field = create_field(2, 2)
    for i in range(2):
        for j in range(2):
            field[i][j] = -1  # Mine every cell
    for i in range(2):
        for j in range(2):
            assert get_hint(field, i, j) == -1  # All cells should return -1

def test_get_hint_for_2x2_field_with_one_mine():
    field = create_field(2, 2)
    field[0][0] = -1  # Place a mine at (0, 0)
    assert get_hint(field, 0, 1) == 1  # Cell (0, 1) should count 1 mine
    assert get_hint(field, 1, 0) == 1  # Cell (1, 0) should count 1 mine
    assert get_hint(field, 1, 1) == 2  # Cell (1, 1) should count 2 mines

def test_get_hint_for_3x3_field_with_mines():
    field = create_field(3, 3)
    field[0][0] = -1  # Place mine at (0, 0)
    field[0][1] = -1  # Place mine at (0, 1)
    assert get_hint(field, 0, 2) == 1  # Cell (0, 2) should count 1 mine
    assert get_hint(field, 1, 0) == 2  # Cell (1, 0) should count 2 mines
    assert get_hint(field, 1, 1) == 2  # Cell (1, 1) should count 2 mines
    assert get_hint(field, 1, 2) == 1  # Cell (1, 2) should count 1 mine
    assert get_hint(field, 2, 0) == 0  # Cell (2, 0) should count 0 mines
    assert get_hint(field, 2, 1) == 0  # Cell (2, 1) should count 0 mines
    assert get_hint(field, 2, 2) == 0  # Cell (2, 2) should count 0 mines

def test_get_hint_for_3x3_field_specific_example():
    field = create_field(3, 3)
    field[0][0] = -1  # Place mine at (0, 0)
    field[0][1] = -1  # Place mine at (0, 1)
    assert get_hint(field, 0, 2) == 1  # Cell (0, 2) has 1 adjacent mine
    assert get_hint(field, 1, 0) == 2  # Cell (1, 0) has 2 adjacent mines
    assert get_hint(field, 1, 1) == 2  # Cell (1, 1) has 2 adjacent mines
    assert get_hint(field, 1, 2) == 1  # Cell (1, 2) has 1 adjacent mine
    assert get_hint(field, 2, 0) == 0  # Cell (2, 0) has 0 adjacent mines
    assert get_hint(field, 2, 1) == 0  # Cell (2, 1) has 0 adjacent mines
    assert get_hint(field, 2, 2) == 0  # Cell (2, 2) has 0 adjacent mines