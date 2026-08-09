# your complete test file
import pytest
from solution import create_field, get_cell_hint

def test_create_field_with_given_dimensions():
    field = create_field(3, 2)
    # Expect a field with 2 rows and 3 columns
    assert len(field) == 2  # 2 rows
    assert len(field[0]) == 3  # 3 columns
    assert len(field[1]) == 3  # 3 columns

def test_empty_field_hints():
    field = create_field(3, 2)
    hints = [get_cell_hint(field, col, row) for row in range(2) for col in range(3)]
    assert hints == [0, 0, 0, 0, 0, 0]  # All cells report 0

def test_mined_cell_reports_mine_marker():
    field = create_field(3, 2)
    field[0][0] = 'mine'  # Place a mine
    assert get_cell_hint(field, 0, 0) == -1  # Mined cell reports -1

def test_all_cells_mined_report_mine_marker():
    field = create_field(2, 2)
    for row in range(2):
        for col in range(2):
            field[row][col] = 'mine'  # Place mines in all cells
    hints = [get_cell_hint(field, col, row) for row in range(2) for col in range(2)]
    assert hints == [-1, -1, -1, -1]  # All cells report -1

def test_safe_cell_reports_adjacent_mines():
    field = create_field(3, 3)
    field[0][0] = 'mine'
    field[0][1] = 'mine'
    hints = [get_cell_hint(field, col, row) for row in range(3) for col in range(3)]
    assert hints == [-1, -1, 1,  # Row 0: both cells are mined, (0,2) has 1 adjacent mine
                     2, 2, 1,  # Row 1: (1,0) and (1,1) have 2 adjacent mines, (1,2) has 1
                     0, 0, 0]  # Row 2: no adjacent mines for any cell

def test_cell_with_no_adjacent_mines_reports_zero():
    field = create_field(3, 3)
    field[0][0] = 'mine'
    hints = [get_cell_hint(field, 1, 1)]  # Check cell (1,1)
    assert hints == [1]  # Cell (1,1) has 1 adjacent mine at (0,0)

def test_2_by_2_field_with_one_mine():
    field = create_field(2, 2)
    field[0][0] = 'mine'
    hints = [get_cell_hint(field, col, row) for row in range(2) for col in range(2)]
    assert hints == [-1, 1,  # Row 0: (0,0) is mined, (0,1) has 1 adjacent mine
                     1, -1]  # Row 1: (1,0) has 1 adjacent mine, (1,1) is mined

def test_2_by_2_field_with_two_mines():
    field = create_field(2, 2)
    field[0][0] = 'mine'
    field[0][1] = 'mine'
    hints = [get_cell_hint(field, col, row) for row in range(2) for col in range(2)]
    assert hints == [-1, -1,  # Row 0: both cells are mined
                     2, 2]    # Row 1: both remaining cells have 2 adjacent mines

def test_2_by_2_field_with_three_mines():
    field = create_field(2, 2)
    field[0][0] = 'mine'
    field[0][1] = 'mine'
    field[1][0] = 'mine'
    hints = [get_cell_hint(field, col, row) for row in range(2) for col in range(2)]
    assert hints == [-1, -1,  # Row 0: both cells are mined
                     -1, 3]   # Row 1: (1,1) has 3 adjacent mines

def test_3_by_3_field_with_mines():
    field = create_field(3, 3)
    field[0][0] = 'mine'
    field[0][1] = 'mine'
    hints = [get_cell_hint(field, col, row) for row in range(3) for col in range(3)]
    assert hints == [-1, -1, 1,  # Row 0: both cells are mined, (0,2) has 1 adjacent mine
                     2, 2, 1,  # Row 1: (1,0) and (1,1) have 2 adjacent mines, (1,2) has 1
                     0, 0, 0]  # Row 2: no adjacent mines for any cell