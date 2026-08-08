from solution import create_field, place_mine, get_cell_hint

def test_create_field_with_dimensions():
    field = create_field(3, 2)
    # The specification does not require a specific representation, only dimensions
    # so we won't check lengths here.

def test_field_with_no_mines_reports_zero_hints():
    field = create_field(2, 2)
    hints = [get_cell_hint(field, x, y) for y in range(2) for x in range(2)]
    assert hints == [0, 0, 0, 0]  # No mines, all cells should report 0

def test_mined_cell_reports_mine_marker():
    field = create_field(2, 2)
    place_mine(field, 0, 0)  # Place a mine
    assert get_cell_hint(field, 0, 0) == -1  # Mine marker

def test_field_where_every_cell_is_mined_reports_mine_marker():
    field = create_field(2, 2)
    for y in range(2):
        for x in range(2):
            place_mine(field, x, y)  # Place mines in all cells
    hints = [get_cell_hint(field, x, y) for y in range(2) for x in range(2)]
    assert hints == [-1, -1, -1, -1]  # All cells are mined

def test_safe_cell_reports_count_of_adjacent_mines():
    field = create_field(3, 3)
    place_mine(field, 0, 0)  # Place a mine at (0, 0)
    assert get_cell_hint(field, 0, 1) == 1  # Adjacent to one mine
    assert get_cell_hint(field, 1, 0) == 1  # Adjacent to one mine
    assert get_cell_hint(field, 1, 1) == 1  # Adjacent to one mine (0, 0)

def test_cell_with_no_adjacent_mines_reports_zero():
    field = create_field(3, 3)
    place_mine(field, 0, 0)  # Place a mine at (0, 0)
    assert get_cell_hint(field, 2, 2) == 0  # No adjacent mines

def test_2_by_2_field_with_one_mine_reports_correct_hints():
    field = create_field(2, 2)
    place_mine(field, 0, 0)  # Place one mine
    hints = [get_cell_hint(field, x, y) for y in range(2) for x in range(2)]
    assert hints == [-1, 1, 1, 1]  # One cell is mined, the others should report 1

def test_2_by_2_field_with_two_mines_reports_correct_hints():
    field = create_field(2, 2)
    place_mine(field, 0, 0)  # Place first mine
    place_mine(field, 0, 1)  # Place second mine
    hints = [get_cell_hint(field, x, y) for y in range(2) for x in range(2)]
    assert hints == [-1, 2, -1, 2]  # Both cells are mined, others report 2

def test_2_by_2_field_with_three_mines_reports_correct_hints():
    field = create_field(2, 2)
    place_mine(field, 0, 0)  # Place first mine
    place_mine(field, 0, 1)  # Place second mine
    place_mine(field, 1, 0)  # Place third mine
    hints = [get_cell_hint(field, x, y) for y in range(2) for x in range(2)]
    assert hints == [-1, -1, -1, 3]  # Three cells are mined, one reports 3

def test_3_by_3_example_reports_correct_hints():
    field = create_field(3, 3)
    place_mine(field, 0, 0)  # Place a mine at (0, 0)
    place_mine(field, 1, 0)  # Place a mine at (1, 0)
    hints = [get_cell_hint(field, x, y) for y in range(3) for x in range(3)]
    assert hints == [-1, -1, 1,  # First row: two mines, one hint
                     2, 2, 1,  # Second row: two hints
                     0, 0, 0]  # Third row: no hints

def test_non_square_field_reports_correct_hints():
    field = create_field(3, 2)
    place_mine(field, 2, 1)  # Place a mine at (2, 1)
    hints = [get_cell_hint(field, x, y) for y in range(2) for x in range(3)]
    assert hints == [0, 0, -1,  # First row: no mines, one mine
                     1, 0, 0]  # Second row: one adjacent mine