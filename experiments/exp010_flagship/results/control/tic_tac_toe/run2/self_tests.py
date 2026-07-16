import pytest
from solution import start_game, make_move, check_winner, is_draw

def test_start_game_creates_blank_board():
    board = start_game()
    # A new game presents a three-by-three board of blank squares
    expected_board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert board == expected_board

def test_start_game_sets_first_player_to_X():
    board, current_player = start_game()
    # X is the first player to move
    assert current_player == 'X'

def test_make_move_marks_square_for_X():
    board, current_player = start_game()
    board, current_player = make_move(board, 0, 0, current_player)
    # A move marks the chosen square with the letter of the player
    expected_board = [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert board == expected_board

def test_make_move_marks_square_for_O():
    board, current_player = start_game()
    board, current_player = make_move(board, 0, 0, current_player)  # X moves first
    board, current_player = make_move(board, 1, 1, current_player)  # O's turn
    # The next move marks the chosen square with O
    expected_board = [['X', ' ', ' '], [' ', 'O', ' '], [' ', ' ', ' ']]
    assert board == expected_board

def test_make_move_passes_turn_to_O():
    board, current_player = start_game()
    board, current_player = make_move(board, 0, 0, current_player)
    # After X's move, the turn passes to O
    assert current_player == 'O'

def test_make_move_passes_turn_to_X():
    board, current_player = start_game()
    board, current_player = make_move(board, 0, 0, current_player)  # X's turn
    board, current_player = make_move(board, 1, 1, current_player)  # O's turn
    # After O's move, the turn passes back to X
    assert current_player == 'X'

def test_check_winner_row_win():
    board = [['X', 'X', 'X'], [' ', 'O', ' '], [' ', ' ', ' ']]
    winner = check_winner(board)
    # Three matching marks across a row win the game for X
    assert winner == 'X'

def test_check_winner_column_win():
    board = [['X', ' ', ' '], ['X', ' ', ' '], ['X', 'O', ' ']]
    winner = check_winner(board)
    # Three matching marks down a column win the game for X
    assert winner == 'X'

def test_check_winner_diagonal_win():
    board = [['X', ' ', 'O'], [' ', 'X', ' '], ['O', ' ', 'X']]
    winner = check_winner(board)
    # Three matching marks along a diagonal win the game for X
    assert winner == 'X'

def test_is_draw_full_board_no_winner():
    board = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'X', 'O']]
    result = is_draw(board)
    # A full board with no winner declares a draw
    assert result is True

def test_is_draw_not_full_board():
    board = [['X', 'O', 'X'], ['X', ' ', 'O'], ['O', 'X', 'O']]
    result = is_draw(board)
    # While open squares remain, the game is not a draw
    assert result is False