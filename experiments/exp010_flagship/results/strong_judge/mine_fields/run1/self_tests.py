from solution import create_field, place_mine, get_hint

def test_create_field_with_zero_mines():
    field = create_field(3, 3)  # Creating a 3x3 field
    # We will ask for hints; all should report 0
    expected_hints = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    actual_hints = [[get_hint(field, col, row) for col in range(3)] for row in range(3)]
    assert actual_hints == expected_hints

def test_create_field_with_mine():
    field = create_field(3, 3)  # Creating a 3x3 field
    place_mine(field, 0, 0)  # Placing a mine at (0, 0)
    # Expected output should have -1 at (0, 0) and 1 surrounding it
    expected_hints = [
        [-1, 1, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    actual_hints = [[get_hint(field, col, row) for col in range(3)] for row in range(3)]
    assert actual_hints == expected_hints

def test_create_field_with_all_cells_mined():
    field = create_field(2, 2)  # Creating a 2x2 field
    place_mine(field, 0, 0)  # Placing a mine at (0, 0)
    place_mine(field, 0, 1)  # Placing a mine at (0, 1)
    place_mine(field, 1, 0)  # Placing a mine at (1, 0)
    place_mine(field, 1, 1)  # Placing a mine at (1, 1)
    # Every cell is mined, so they all report -1
    expected_hints = [
        [-1, -1],
        [-1, -1]
    ]
    actual_hints = [[get_hint(field, col, row) for col in range(2)] for row in range(2)]
    assert actual_hints == expected_hints

def test_safe_cell_with_no_adjacent_mines():
    field = create_field(3, 3)  # Creating a 3x3 field
    place_mine(field, 1, 1)  # Placing a mine at (1, 1)
    # All cells surrounding (1,1) should report 1
    expected_hints = [
        [1, 1, 1],
        [1, -1, 1],
        [1, 1, 1]
    ]
    actual_hints = [[get_hint(field, col, row) for col in range(3)] for row in range(3)]
    assert actual_hints == expected_hints

def test_2_by_2_field_with_one_mine():
    field = create_field(2, 2)  # Creating a 2x2 field
    place_mine(field, 0, 0)  # Placing a mine at (0, 0)
    # Each of the three remaining cells should report 1
    expected_hints = [
        [-1, 1],
        [1, 1]
    ]
    actual_hints = [[get_hint(field, col, row) for col in range(2)] for row in range(2)]
    assert actual_hints == expected_hints

def test_2_by_2_field_with_two_mines():
    field = create_field(2, 2)  # Creating a 2x2 field
    place_mine(field, 0, 0)  # Placing a mine at (0, 0)
    place_mine(field, 0, 1)  # Placing a mine at (0, 1)
    # With 2 mines, each remaining cell (1, 0) and (1, 1) should report 2
    expected_hints = [
        [-1, -1],
        [2, 2]
    ]
    actual_hints = [[get_hint(field, col, row) for col in range(2)] for row in range(2)]
    assert actual_hints == expected_hints

def test_2_by_2_field_with_three_mines():
    field = create_field(2, 2)  # Creating a 2x2 field
    place_mine(field, 0, 0)  # Placing a mine at (0, 0)
    place_mine(field, 0, 1)  # Placing a mine at (0, 1)
    place_mine(field, 1, 0)  # Placing a mine at (1, 0)
    # Only the remaining cell (1, 1) should report 3
    expected_hints = [
        [-1, -1],
        [-1, 3]
    ]
    actual_hints = [[get_hint(field, col, row) for col in range(2)] for row in range(2)]
    assert actual_hints == expected_hints

def test_3_by_3_example():
    field = create_field(3, 3)  # Creating a 3x3 field
    place_mine(field, 0, 0)  # Placing a mine at (0, 0)
    place_mine(field, 1, 0)  # Placing a mine at (1, 0)
    # Expected result for the remaining cells based on the mines placed
    expected_hints = [
        [-1, -1, 1],
        [2, 2, 1],
        [0, 0, 0]
    ]
    actual_hints = [[get_hint(field, col, row) for col in range(3)] for row in range(3)]
    assert actual_hints == expected_hints

def test_non_square_field():
    field = create_field(4, 2)  # Creating a 4x2 field
    place_mine(field, 0, 0)  # Placing a mine at (0, 0)
    # We will ask for hints; only the first cell should report -1, the rest should be 1
    expected_hints = [
        [-1, 1, 0, 0],
        [1, 0, 0, 0]
    ]
    actual_hints = [[get_hint(field, col, row) for col in range(4)] for row in range(2)]
    assert actual_hints == expected_hints

def test_coordinate_order():
    field = create_field(3, 3)  # Creating a 3x3 field
    # Checking top-left corner for coordinates (0, 0) should be correct
    place_mine(field, 0, 0)  # Placing a mine at (0, 0)
    assert get_hint(field, 0, 0) == -1  # Mine should report -1
    assert get_hint(field, 1, 0) == 1  # Right cell should report 1
    assert get_hint(field, 0, 1) == 1  # Below cell should report 1