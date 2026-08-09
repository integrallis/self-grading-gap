# test_tic_tac_toe.py

from solution import start_game, make_move, check_winner, is_draw

def test_start_game_creates_empty_board():
    # Expect a 3x3 board of blank squares (spaces)
    board, current_player = start_game()  # Assuming start_game() returns the board and current player
    expected_board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert board == expected_board  # Verify the board is empty

def test_start_game_sets_first_player_to_X():
    # Expect the first player to be 'X'
    board, current_player = start_game()
    expected_first_player = 'X'
    assert current_player == expected_first_player  # Verify that the first player is X

def test_make_move_marks_square_with_X():
    # Start a game and make a move for player X
    board, current_player = start_game()
    board = make_move(board, 0, 0)  # X moves to (0, 0)
    expected_board = [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert board == expected_board  # Verify the move was marked correctly

def test_make_move_marks_square_with_O():
    # Start a game, make a move for X, then O
    board, current_player = start_game()
    board = make_move(board, 0, 0)  # X moves to (0, 0)
    board = make_move(board, 1, 1)  # O moves to (1, 1)
    expected_board = [['X', ' ', ' '], [' ', 'O', ' '], [' ', ' ', ' ']]
    assert board == expected_board  # Verify the board after both moves

def test_make_move_passes_turn_to_next_player():
    # Start a game and make a move for X
    board, current_player = start_game()
    board = make_move(board, 0, 0)  # X moves
    assert current_player == 'X'  # Verify the current player is X
    board, current_player = make_move(board, 1, 1)  # O moves
    assert current_player == 'O'  # Verify the current player is O

def test_make_move_non_symmetric_coordinates():
    # Start a game and make a move in a non-symmetric position
    board, current_player = start_game()
    board = make_move(board, 0, 2)  # X moves to (0, 2)
    expected_board = [[' ', ' ', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert board == expected_board  # Verify the move was marked correctly

def test_check_winner_row_win_top():
    # Check winner when X has three in a row (top row)
    board = [['X', 'X', 'X'], ['O', ' ', ' '], [' ', ' ', ' ']]
    winner = check_winner(board)
    expected_winner = 'X'  # X wins
    assert winner == expected_winner  # Verify the winner is X

def test_check_winner_row_win_middle():
    # Check winner when X has three in a row (middle row)
    board = [['O', ' ', ' '], ['X', 'X', 'X'], [' ', ' ', ' ']]
    winner = check_winner(board)
    expected_winner = 'X'  # X wins
    assert winner == expected_winner  # Verify the winner is X

def test_check_winner_row_win_bottom():
    # Check winner when X has three in a row (bottom row)
    board = [['O', ' ', ' '], [' ', ' ', ' '], ['X', 'X', 'X']]
    winner = check_winner(board)
    expected_winner = 'X'  # X wins
    assert winner == expected_winner  # Verify the winner is X

def test_check_winner_column_win_left():
    # Check winner when X has three in a column (left column)
    board = [['X', 'O', ' '], ['X', ' ', ' '], ['X', ' ', 'O']]
    winner = check_winner(board)
    expected_winner = 'X'  # X wins
    assert winner == expected_winner  # Verify the winner is X

def test_check_winner_column_win_middle():
    # Check winner when O has three in a column (middle column)
    board = [['X', 'O', ' '], [' ', 'O', ' '], [' ', 'O', 'X']]
    winner = check_winner(board)
    expected_winner = 'O'  # O wins
    assert winner == expected_winner  # Verify the winner is O

def test_check_winner_column_win_right():
    # Check winner when X has three in a column (right column)
    board = [[' ', 'O', 'X'], [' ', ' ', 'X'], [' ', ' ', 'X']]
    winner = check_winner(board)
    expected_winner = 'X'  # X wins
    assert winner == expected_winner  # Verify the winner is X

def test_check_winner_diagonal_win():
    # Check winner when X has three in a diagonal
    board = [['X', ' ', 'O'], [' ', 'X', ' '], ['O', ' ', 'X']]
    winner = check_winner(board)
    expected_winner = 'X'  # X wins
    assert winner == expected_winner  # Verify the winner is X

def test_check_winner_anti_diagonal_win():
    # Check winner when O has three in the anti-diagonal
    board = [['O', ' ', 'X'], [' ', 'O', ' '], ['X', ' ', 'O']]
    winner = check_winner(board)
    expected_winner = 'O'  # O wins
    assert winner == expected_winner  # Verify the winner is O

def test_is_draw_when_board_full_no_winner():
    # Check draw when board is full and no winner
    board = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'X', 'O']]
    draw_status = is_draw(board)  # Check if the game is a draw
    winner = check_winner(board)
    assert draw_status is True  # The game should be declared a draw
    assert winner is None  # Verify that there is no winner

def test_is_draw_when_board_not_full():
    # Check draw status when the board is not full
    board = [['X', 'O', ' '], ['X', 'X', 'O'], ['O', 'X', 'O']]
    draw_status = is_draw(board)
    assert draw_status is False  # The game should not be a draw

def test_full_board_with_winning_line_is_not_draw():
    # Check that a full board with a winning line is not declared a draw
    board = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'X', 'X']]
    winner = check_winner(board)
    draw_status = is_draw(board)
    assert winner == 'X'  # X should be the winner
    assert draw_status is False  # The game should not be a draw

def test_start_second_game_after_first():
    # Start a game, make a move, then start a new game
    board, current_player = start_game()
    board = make_move(board, 0, 0)  # X moves
    new_board, new_current_player = start_game()  # Start a new game
    expected_new_board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    expected_new_player = 'X'
    assert new_board == expected_new_board  # Verify the new board is empty
    assert new_current_player == expected_new_player  # Verify the new game starts with X