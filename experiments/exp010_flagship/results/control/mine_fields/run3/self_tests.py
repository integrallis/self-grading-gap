from solution import create_field, get_hint

def test_create_field_with_given_dimensions():
    # Create a 3x3 field
    field = create_field(3, 3)
    assert len(field) == 3  # 3 rows
    assert all(len(row) == 3 for row in field)  # each row has 3 columns

def test_empty_field_reports_zero_hints():
    # Create a 2x2 field
    field = create_field(2, 2)
    # Check all cells report 0
    for row in field:
        for cell in row:
            assert get_hint(cell) == 0  # No mines, should report 0

def test_mined_cell_reports_mine_marker():
    # Create a 1x1 field with a mine
    field = create_field(1, 1)
    field[0][0] = -1  # Place a mine
    assert get_hint(field[0][0]) == -1  # Mine should report -1

def test_field_with_all_mined_cells_reports_mine_marker():
    # Create a 2x2 field and mine all cells
    field = create_field(2, 2)
    for row in range(2):
        for col in range(2):
            field[row][col] = -1  # Place a mine
    for row in field:
        for cell in row:
            assert get_hint(cell) == -1  # All cells should report -1

def test_safe_cell_reports_count_of_neighbouring_mines():
    # Create a 3x3 field with specific mine placements
    field = create_field(3, 3)
    field[0][0] = -1  # Mine at (0,0)
    field[0][1] = -1  # Mine at (0,1)
    # The middle cell (1,1) should report 2 (mines at (0,0) and (0,1))
    assert get_hint(field[1][1]) == 2  # Mine count around (1,1) is 2

def test_mine_free_cell_with_no_adjacent_mines_reports_zero():
    # Create a 3x3 field with one mine
    field = create_field(3, 3)
    field[0][0] = -1  # Mine at (0,0)
    assert get_hint(field[1][1]) == 1  # Cell (1,1) has 1 adjacent mine
    assert get_hint(field[2][2]) == 0  # Cell (2,2) has no adjacent mines

def test_2x2_field_counts_mines_correctly():
    # Create a 2x2 field with one mine
    field = create_field(2, 2)
    field[0][0] = -1  # Mine at (0,0)
    # (0,1) should report 1, (1,0) should report 1, (1,1) should report 1
    assert get_hint(field[0][1]) == 1  # (0,1) has 1 adjacent mine
    assert get_hint(field[1][0]) == 1  # (1,0) has 1 adjacent mine
    assert get_hint(field[1][1]) == 1  # (1,1) has 1 adjacent mine

def test_3x3_example_counts_mines_correctly():
    # Create a 3x3 field with specific mine placements
    field = create_field(3, 3)
    field[0][0] = -1  # Mine at (0,0)
    field[0][1] = -1  # Mine at (0,1)
    # Check the expected hints
    assert get_hint(field[0][2]) == 1  # (0,2) has 1 adjacent mine
    assert get_hint(field[1][0]) == 2  # (1,0) has 2 adjacent mines
    assert get_hint(field[1][1]) == 2  # (1,1) has 2 adjacent mines
    assert get_hint(field[1][2]) == 1  # (1,2) has 1 adjacent mine
    assert get_hint(field[2][0]) == 0  # (2,0) has 0 adjacent mines
    assert get_hint(field[2][1]) == 0  # (2,1) has 0 adjacent mines
    assert get_hint(field[2][2]) == 0  # (2,2) has 0 adjacent mines

def test_3x3_field_counts_mines_with_example():
    # Create a 3x3 field with specific mine placements
    field = create_field(3, 3)
    field[0][0] = -1  # Mine at (0,0)
    field[0][1] = -1  # Mine at (0,1)
    # Check the expected hints based on the specification
    assert get_hint(field[0][2]) == 1  # (0,2) has 1 adjacent mine
    assert get_hint(field[1][0]) == 2  # (1,0) has 2 adjacent mines
    assert get_hint(field[1][1]) == 2  # (1,1) has 2 adjacent mines
    assert get_hint(field[1][2]) == 1  # (1,2) has 1 adjacent mine
    assert get_hint(field[2][0]) == 0  # (2,0) has 0 adjacent mines
    assert get_hint(field[2][1]) == 0  # (2,1) has 0 adjacent mines
    assert get_hint(field[2][2]) == 0  # (2,2) has 0 adjacent mines