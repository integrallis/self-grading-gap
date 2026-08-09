# test_minesweeper.py

from solution import create_field, place_mine, get_cell_hint

def test_create_field_with_no_mines():
    field = create_field(3, 2)  # Creating a 3x2 field
    # Check that the field has been created; details on internal representation are not required
    for row in range(2):
        for column in range(3):
            assert get_cell_hint(field, column, row) == 0  # Expecting all cells to report 0

def test_create_field_with_mines():
    field = create_field(3, 3)  # Creating a 3x3 field
    place_mine(field, 0, 0)  # Placing a mine at (0, 0)
    place_mine(field, 0, 1)  # Placing a mine at (0, 1)
    
    # Expecting counts based on the mines placed
    assert get_cell_hint(field, 0, 0) == -1  # Mine
    assert get_cell_hint(field, 0, 1) == -1  # Mine
    assert get_cell_hint(field, 0, 2) == 1   # One mine adjacent
    assert get_cell_hint(field, 1, 0) == 2   # Two mines adjacent
    assert get_cell_hint(field, 1, 1) == 2   # Two mines adjacent
    assert get_cell_hint(field, 1, 2) == 1   # One mine adjacent
    assert get_cell_hint(field, 2, 0) == 0   # No mines adjacent
    assert get_cell_hint(field, 2, 1) == 0   # No mines adjacent
    assert get_cell_hint(field, 2, 2) == 0   # No mines adjacent

def test_cell_with_no_adjacent_mines():
    field = create_field(3, 3)  # Creating a 3x3 field
    # Expecting a cell with no adjacent mines to return 0
    assert get_cell_hint(field, 2, 2) == 0  # Bottom-right corner

def test_2x2_field_with_one_mine():
    field = create_field(2, 2)  # Creating a 2x2 field
    place_mine(field, 0, 0)  # Placing a mine
    # Expecting remaining cells to report 1 each, since they are adjacent to one mine
    assert get_cell_hint(field, 0, 1) == 1  # One mine adjacent
    assert get_cell_hint(field, 1, 0) == 1  # One mine adjacent
    assert get_cell_hint(field, 1, 1) == 1  # One mine adjacent

def test_2x2_field_with_two_mines():
    field = create_field(2, 2)  # Creating a 2x2 field
    place_mine(field, 0, 0)  # Mine
    place_mine(field, 0, 1)  # Mine
    # Expecting remaining cells to report 2 since they have two adjacent mines
    assert get_cell_hint(field, 1, 0) == 2  # Two mines adjacent
    assert get_cell_hint(field, 1, 1) == 2  # Two mines adjacent

def test_2x2_field_with_three_mines():
    field = create_field(2, 2)  # Creating a 2x2 field
    place_mine(field, 0, 0)  # Mine
    place_mine(field, 0, 1)  # Mine
    place_mine(field, 1, 0)  # Mine
    # Expecting the remaining cell to report 3 since it has three adjacent mines
    assert get_cell_hint(field, 1, 1) == 3  # Three mines adjacent

def test_all_cells_mined():
    field = create_field(3, 3)  # Creating a 3x3 field
    for row in range(3):
        for column in range(3):
            place_mine(field, column, row)  # Mine at every cell
    # Expecting every cell to report -1
    for row in range(3):
        for column in range(3):
            assert get_cell_hint(field, column, row) == -1  # All cells are mines

def test_3x3_field_example():
    field = create_field(3, 3)  # Creating a 3x3 field
    place_mine(field, 0, 0)  # Mine at (0,0)
    place_mine(field, 1, 0)  # Mine at (1,0)
    # Expecting counts based on the specified example
    assert get_cell_hint(field, 0, 0) == -1  # Mine
    assert get_cell_hint(field, 1, 0) == -1  # Mine
    assert get_cell_hint(field, 2, 0) == 1   # One mine adjacent
    assert get_cell_hint(field, 0, 1) == 2   # Two mines adjacent
    assert get_cell_hint(field, 1, 1) == 2   # Two mines adjacent
    assert get_cell_hint(field, 2, 1) == 1   # One mine adjacent
    assert get_cell_hint(field, 0, 2) == 0   # No mines adjacent
    assert get_cell_hint(field, 1, 2) == 0   # No mines adjacent
    assert get_cell_hint(field, 2, 2) == 0   # No mines adjacent