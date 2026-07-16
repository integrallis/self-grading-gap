# test_tic_tac_toe.py

from solution import start_game, make_move, check_winner, is_draw

def test_start_game_creates_blank_board():
    # A fresh game should have a 3x3 board with all squares blank
    board = start_game()
    expected_board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]  # 3x3 blank board
    assert board == expected_board

def test_start_game_sets_first_player_to_X():
    # The first player to move should be X
    board, current_player = start_game()
    assert current_player == 'X'  # X is the first player

def test_make_move_marks_square():
    # A move should mark the chosen square with the player's letter
    board, current_player = start_game()
    board = make_move(board, current_player, 0, 0)  # X makes a move at (0, 0)
    expected_board = [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]  # X has marked the top-left square
    assert board == expected_board

def test_make_move_passes_turn():
    # After a move, the turn should pass to the other player
    board, current_player = start_game()
    board = make_move(board, current_player, 0, 0)  # X makes a move
    current_player = 'O'  # O is next
    board = make_move(board, current_player, 0, 1)  # O makes a move
    expected_board = [['X', 'O', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]  # O has marked (0, 1)
    assert board == expected_board

def test_check_winner_horizontal():
    # A player wins if they have three in a row horizontally
    board = [['X', 'X', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']]
    winner = check_winner(board)
    assert winner == 'X'  # X wins

def test_check_winner_vertical():
    # A player wins if they have three in a row vertically
    board = [['X', ' ', ' '], ['X', ' ', ' '], ['X', ' ', ' ']]
    winner = check_winner(board)
    assert winner == 'X'  # X wins

def test_check_winner_diagonal():
    # A player wins if they have three in a row diagonally
    board = [['X', ' ', 'O'], [' ', 'X', ' '], ['O', ' ', 'X']]
    winner = check_winner(board)
    assert winner == 'X'  # X wins

def test_is_draw_full_board_no_winner():
    # A full board with no winner should be declared a draw
    board = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'X', 'O']]
    draw = is_draw(board)
    assert draw is True  # The game is a draw

def test_is_draw_still_open_squares():
    # If there are still open squares, the game should not be a draw
    board = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', ' ', 'O']]
    draw = is_draw(board)
    assert draw is False  # The game is not a draw