# test_tic_tac_toe.py

from solution import start_game, make_move, check_winner, check_draw

def test_start_game_creates_blank_board():
    # A new game should present a three-by-three board of blank squares
    board, current_player = start_game()
    expected_board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert board == expected_board

def test_start_game_first_player_is_x():
    # X is the first player to move
    board, current_player = start_game()
    assert current_player == 'X'

def test_make_move_marks_square_for_x():
    # A move marks the chosen square with the player's letter (X)
    board, current_player = start_game()
    board, current_player = make_move(board, current_player, 0, 0)  # X moves
    expected_board = [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert board == expected_board

def test_make_move_marks_square_for_o():
    # A move marks the chosen square with the player's letter (O)
    board, current_player = start_game()
    board, current_player = make_move(board, current_player, 0, 0)  # X moves
    board, current_player = make_move(board, current_player, 0, 1)  # O moves
    expected_board = [['X', 'O', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert board == expected_board

def test_make_move_alternates_turns():
    # After each move the turn passes to the other player
    board, current_player = start_game()
    board, current_player = make_move(board, current_player, 0, 0)  # X moves
    assert current_player == 'O'  # Next turn should be O
    board, current_player = make_move(board, current_player, 0, 1)  # O moves
    assert current_player == 'X'  # Next turn should go back to X

def test_make_move_marks_square_at_non_symmetric_coordinates():
    # A move marks the chosen square with the player's letter at (1,2)
    board, current_player = start_game()
    board, current_player = make_move(board, current_player, 1, 2)  # X moves
    expected_board = [[' ', ' ', ' '], [' ', ' ', 'X'], [' ', ' ', ' ']]
    assert board == expected_board

def test_check_winner_row_win():
    # Three matching marks across a row win the game for that player
    board = [['X', 'X', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']]
    winner = check_winner(board)
    assert winner == 'X'  # X wins

def test_check_winner_column_win():
    # Three matching marks down a column win the game for that player
    board = [['O', ' ', ' '], ['O', ' ', ' '], ['O', ' ', ' ']]
    winner = check_winner(board)
    assert winner == 'O'  # O wins

def test_check_winner_diagonal_win():
    # Three matching marks along either diagonal win the game
    board = [['X', ' ', 'O'], [' ', 'X', ' '], ['O', ' ', 'X']]
    winner = check_winner(board)
    assert winner == 'X'  # X wins

def test_check_winner_opposite_diagonal_win():
    # Three matching marks along the opposite diagonal win the game
    board = [['O', ' ', 'X'], [' ', 'X', ' '], ['X', ' ', 'O']]
    winner = check_winner(board)
    assert winner == 'X'  # X wins

def test_check_draw_no_winner_full_board():
    # When every square is filled and no line is complete, the game reports a draw
    board = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'X', 'O']]
    winner = check_winner(board)
    assert winner is None  # No winner
    
    draw = check_draw(board)
    assert draw is True  # It should declare a draw

def test_check_draw_not_a_draw_with_open_squares():
    # While open squares remain, the game is not a draw
    board = [['X', 'O', 'X'], ['X', ' ', 'O'], ['O', 'X', 'O']]
    winner = check_winner(board)
    assert winner is None  # No winner
    
    draw = check_draw(board)
    assert draw is False  # It should not declare a draw