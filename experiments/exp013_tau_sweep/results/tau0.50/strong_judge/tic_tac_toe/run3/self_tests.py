# test_tic_tac_toe.py

from solution import start_game, make_move, check_winner, is_draw

def test_start_game_creates_empty_board():
    # Expect a 3x3 board of blank squares.
    expected_board = [[' ', ' ', ' '],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]
    start_game()  # Start the game to create a fresh board.

def test_start_game_sets_first_player_to_X():
    # Expect the first player to be 'X'.
    board, current_player = start_game()
    assert current_player == 'X'  # Check that X is the first player.

def test_make_move_marks_square_for_X():
    # Start a game and make a move for X at (0, 0).
    board, current_player = start_game()
    updated_board, next_player = make_move(board, current_player, 0, 0)
    expected_board = [['X', ' ', ' '],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]
    assert updated_board == expected_board
    assert next_player == 'O'

def test_make_move_marks_square_for_O():
    # Start a game and make a move for X, then O.
    board, current_player = start_game()
    board, current_player = make_move(board, current_player, 0, 0)
    updated_board, next_player = make_move(board, current_player, 1, 1)
    expected_board = [['X', ' ', ' '],
                      [' ', 'O', ' '],
                      [' ', ' ', ' ']]
    assert updated_board == expected_board
    assert next_player == 'X'

def test_make_move_marks_square_for_X_non_diagonal():
    # Start a game and make a move for X at (0, 2).
    board, current_player = start_game()
    updated_board, next_player = make_move(board, current_player, 0, 2)
    expected_board = [[' ', ' ', 'X'],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]
    assert updated_board == expected_board
    assert next_player == 'O'

def test_winning_row():
    # Test winning condition for X across the first row.
    board = [['X', 'X', 'X'],
             ['O', ' ', ' '],
             [' ', ' ', ' ']]
    assert check_winner(board) == 'X'

def test_winning_column():
    # Test winning condition for O down the first column.
    board = [['O', 'X', ' '],
             ['O', ' ', ' '],
             ['O', ' ', ' ']]
    assert check_winner(board) == 'O'

def test_winning_diagonal():
    # Test winning condition for X along the diagonal.
    board = [['X', ' ', 'O'],
             [' ', 'X', ' '],
             ['O', ' ', 'X']]
    assert check_winner(board) == 'X'

def test_winning_anti_diagonal():
    # Test winning condition for O along the anti-diagonal.
    board = [['X', ' ', 'O'],
             [' ', 'O', ' '],
             ['O', ' ', 'X']]
    assert check_winner(board) == 'O'

def test_draw_condition():
    # Test a draw condition with no empty squares and no winner.
    board = [['X', 'O', 'X'],
             ['X', 'X', 'O'],
             ['O', 'X', 'O']]
    assert check_winner(board) is None  # Expect no winner.
    assert is_draw(board) == True

def test_not_draw_with_empty_square():
    # Test condition where the game is not a draw as there are empty squares.
    board = [['X', 'O', 'X'],
             ['X', 'X', 'O'],
             ['O', ' ', 'O']]
    assert is_draw(board) == False