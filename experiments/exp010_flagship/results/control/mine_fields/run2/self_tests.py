# test_minesweeper.py

from solution import create_field, get_hint

def test_create_field_with_zero_mines():
    field = create_field(3, 3)  # Create a 3x3 field
    expected = [[0, 0, 0],      # All cells should report 0 as there are no mines
                [0, 0, 0],
                [0, 0, 0]]
    assert field == expected

def test_create_field_with_mines():
    field = create_field(3, 3)
    field[0][0] = -1  # Place a mine at (0, 0)
    field[0][1] = -1  # Place a mine at (0, 1)
    expected = [[-1, -1, 0],     # Mines at (0,0) and (0,1)
                [1, 1, 0],      # (1,0) has 1 neighbour, (1,1) has 2 neighbours
                [0, 0, 0]]      # Remaining cells have 0 neighbours
    assert field == expected

def test_hint_for_mined_cell():
    field = create_field(3, 3)
    field[1][1] = -1  # Place a mine at (1, 1)
    hint = get_hint(field, 1, 1)  # Hint for mined cell
    assert hint == -1  # Mined cell should return -1

def test_hint_for_safe_cell_with_no_adjacent_mines():
    field = create_field(2, 2)
    field[0][0] = -1  # Place a mine at (0, 0)
    hint = get_hint(field, 1, 1)  # Hint for (1, 1) which is safe
    assert hint == 0  # (1,1) has no adjacent mines, so should report 0

def test_hint_for_safe_cell_with_adjacent_mines():
    field = create_field(3, 3)
    field[0][0] = -1  # Mine at (0, 0)
    field[0][1] = -1  # Mine at (0, 1)
    hint = get_hint(field, 1, 0)  # Hint for (1, 0)
    assert hint == 2  # (1,0) has 2 mines adjacent

def test_hint_for_cell_with_no_adjacent_mines():
    field = create_field(3, 3)
    hint = get_hint(field, 2, 2)  # Hint for (2, 2) which is safe
    assert hint == 0  # No adjacent mines

def test_all_cells_mined():
    field = create_field(2, 2)
    field[0][0] = -1
    field[0][1] = -1
    field[1][0] = -1
    field[1][1] = -1
    expected = [[-1, -1], [-1, -1]]  # All cells should be mined
    assert field == expected

def test_counting_adjacent_mines_in_2x2_field():
    field = create_field(2, 2)
    field[0][0] = -1  # Mine at (0, 0)
    field[0][1] = -1  # Mine at (0, 1)
    hint1 = get_hint(field, 0, 1)  # Check (0, 1)
    hint2 = get_hint(field, 1, 1)  # Check (1, 1)
    hint3 = get_hint(field, 1, 0)  # Check (1, 0)
    assert hint1 == 2  # (0,1) has 2 mines adjacent
    assert hint2 == 1  # (1,1) has 1 mine adjacent
    assert hint3 == 1  # (1,0) has 1 mine adjacent

def test_worked_example_3x3_field():
    field = create_field(3, 3)
    field[0][0] = -1  # Place mine at (0, 0)
    field[0][1] = -1  # Place mine at (0, 1)
    expected_hints = [[-1, -1, 1],  # (-1 at (0,0) and (0,1), (0,2) has 1 adjacent mine)
                      [2, 2, 1],   # (1,0) and (1,1) each have 2 adjacent mines, (1,2) has 1
                      [0, 0, 0]]   # All remaining cells have no adjacent mines
    for row in range(3):
        for col in range(3):
            assert get_hint(field, row, col) == expected_hints[row][col]

def test_counting_all_mined_cells_in_4x4_field():
    field = create_field(4, 4)
    for row in range(4):
        for col in range(4):
            field[row][col] = -1  # Place a mine in every cell
    expected = [[-1, -1, -1, -1],
                [-1, -1, -1, -1],
                [-1, -1, -1, -1],
                [-1, -1, -1, -1]]  # All cells should report -1
    assert field == expected