from solution import create_field, get_hint

def test_create_field_with_given_dimensions():
    # Test creating a field with width 3 and height 2
    field = create_field(3, 2)
    assert len(field) == 2  # Height should be 2
    assert len(field[0]) == 3  # Width should be 3

def test_field_with_no_mines_reports_zero():
    # Test that all cells report 0 when no mines are placed
    field = create_field(3, 2)
    hints = [get_hint(field, col, row) for row in range(2) for col in range(3)]
    assert all(hint == 0 for hint in hints)  # All cells should report 0

def test_mined_cell_reports_mine_marker():
    # Test that a cell with a mine reports -1
    field = create_field(3, 2)
    field[0][0] = 'M'  # Place a mine
    assert get_hint(field, 0, 0) == -1  # The mined cell should report -1

def test_all_cells_mined_report_mine_marker():
    # Test that all cells report -1 when all are mined
    field = create_field(2, 2)
    for row in range(2):
        for col in range(2):
            field[row][col] = 'M'  # Place mines in all cells
    hints = [get_hint(field, col, row) for row in range(2) for col in range(2)]
    assert all(hint == -1 for hint in hints)  # All cells should report -1

def test_safe_cell_counts_adjacent_mines():
    # Test that a cell reports the number of adjacent mines
    field = create_field(3, 3)
    field[0][0] = 'M'  # Place a mine
    field[0][1] = 'M'  # Place another mine
    hints = [
        get_hint(field, 0, 0),  # Mine cell
        get_hint(field, 0, 1),  # Mine cell
        get_hint(field, 0, 2),  # Safe cell, adjacent mines: 2
        get_hint(field, 1, 0),  # Safe cell, adjacent mines: 2
        get_hint(field, 1, 1),  # Safe cell, adjacent mines: 2
        get_hint(field, 1, 2),  # Safe cell, adjacent mines: 1
        get_hint(field, 2, 0),  # Safe cell, adjacent mines: 0
        get_hint(field, 2, 1),  # Safe cell, adjacent mines: 0
        get_hint(field, 2, 2)   # Safe cell, adjacent mines: 0
    ]
    assert hints == [-1, -1, 2, 2, 2, 1, 0, 0, 0]  # Correct expected hints

def test_2x2_field_with_one_mine():
    # Test 2x2 field with one mine
    field = create_field(2, 2)
    field[0][0] = 'M'  # Place a mine
    hints = [
        get_hint(field, 0, 0),  # Mine cell
        get_hint(field, 0, 1),  # Safe cell, adjacent mines: 1
        get_hint(field, 1, 0),  # Safe cell, adjacent mines: 1
        get_hint(field, 1, 1)   # Safe cell, adjacent mines: 1
    ]
    assert hints == [-1, 1, 1, 1]  # Expected hints

def test_2x2_field_with_two_mines():
    # Test 2x2 field with two mines
    field = create_field(2, 2)
    field[0][0] = 'M'  # Place a mine
    field[0][1] = 'M'  # Place another mine
    hints = [
        get_hint(field, 0, 0),  # Mine cell
        get_hint(field, 0, 1),  # Mine cell
        get_hint(field, 1, 0),  # Safe cell, adjacent mines: 2
        get_hint(field, 1, 1)   # Safe cell, adjacent mines: 2
    ]
    assert hints == [-1, -1, 2, 2]  # Expected hints

def test_2x2_field_with_three_mines():
    # Test 2x2 field with three mines
    field = create_field(2, 2)
    field[0][0] = 'M'  # Place a mine
    field[0][1] = 'M'  # Place another mine
    field[1][0] = 'M'  # Place a third mine
    hints = [
        get_hint(field, 0, 0),  # Mine cell
        get_hint(field, 0, 1),  # Mine cell
        get_hint(field, 1, 0),  # Mine cell
        get_hint(field, 1, 1)   # Safe cell, adjacent mines: 3
    ]
    assert hints == [-1, -1, -1, 3]  # Expected hints

def test_safe_cell_with_no_adjacent_mines():
    # Test that a cell reports 0 if no adjacent cells have mines
    field = create_field(3, 3)
    field[0][0] = 'M'  # Place a mine
    hints = [
        get_hint(field, 1, 1),  # Safe cell in center, adjacent mines: 1
        get_hint(field, 0, 0),  # Mine cell
        get_hint(field, 2, 2)   # Safe cell in corner, adjacent mines: 0
    ]
    assert hints == [1, -1, 0]  # Center should report 1, and corners as well

def test_safe_cell_with_no_adjacent_mines_elsewhere():
    # Test that a cell reports 0 if no adjacent cells have mines
    field = create_field(3, 3)
    field[0][0] = 'M'  # Place a mine
    hints = [
        get_hint(field, 0, 1),  # Safe cell, adjacent mines: 1
        get_hint(field, 1, 1),  # Safe cell, adjacent mines: 1
        get_hint(field, 2, 2)   # Safe cell in corner, adjacent mines: 0
    ]
    assert hints == [1, 1, 0]  # Center should report 1, and corner should report 0