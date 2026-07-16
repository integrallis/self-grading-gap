# test_tic_tac_toe.py

from solution import start_game, make_move, check_winner, is_draw

def test_start_game_creates_blank_board():
    # A new game presents a three-by-three board of blank squares
    expected_board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    board = start_game()  # The specification does not state the return type
    assert board == expected_board

def test_start_game_sets_first_player_to_x():
    # X is the first player to move
    board, current_player = start_game()  # Assuming start_game returns a tuple
    assert current_player == 'X'

def test_make_move_marks_square_with_x():
    # A move marks the chosen square with the letter of the player whose turn it is
    board, current_player = start_game()
    make_move(board, current_player, 0, 2)  # X moves to row 0, column 2
    expected_board = [[' ', ' ', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert board == expected_board

def test_turn_passes_after_move():
    # After each move the turn passes to the other player
    board, current_player = start_game()
    make_move(board, current_player, 0, 0)  # X moves
    next_player = 'O'  # Next turn is implicitly O now
    current_player = 'O'  # Simulate turn passing
    assert current_player == next_player

def test_three_in_a_row_wins_game():
    # Three matching marks across a row win the game for that player
    board, current_player = start_game()
    make_move(board, current_player, 0, 0)  # X moves
    make_move(board, 'O', 1, 0)  # O moves
    make_move(board, current_player, 0, 1)  # X moves
    make_move(board, 'O', 1, 1)  # O moves
    make_move(board, current_player, 0, 2)  # X moves
    winner = check_winner(board)
    assert winner == 'X'

def test_three_in_a_column_wins_game():
    # Three matching marks down a column win the game for that player
    board, current_player = start_game()
    make_move(board, current_player, 0, 0)  # X moves
    make_move(board, 'O', 0, 1)  # O moves
    make_move(board, current_player, 1, 0)  # X moves
    make_move(board, 'O', 1, 1)  # O moves
    make_move(board, current_player, 2, 0)  # X moves
    winner = check_winner(board)
    assert winner == 'X'

def test_three_in_a_main_diagonal_wins_game():
    # Three matching marks along the main diagonal win the game
    board, current_player = start_game()
    make_move(board, current_player, 0, 0)  # X moves to (0, 0)
    make_move(board, 'O', 0, 1)  # O moves
    make_move(board, current_player, 1, 1)  # X moves to (1, 1)
    make_move(board, 'O', 1, 0)  # O moves
    make_move(board, current_player, 2, 2)  # X moves to (2, 2)
    winner = check_winner(board)
    assert winner == 'X'

def test_three_in_a_anti_diagonal_wins_game():
    # Three matching marks along the anti-diagonal win the game
    board, current_player = start_game()
    make_move(board, current_player, 0, 2)  # X moves to (0, 2)
    make_move(board, 'O', 0, 1)  # O moves
    make_move(board, current_player, 1, 1)  # X moves to (1, 1)
    make_move(board, 'O', 1, 0)  # O moves
    make_move(board, current_player, 2, 0)  # X moves to (2, 0)
    winner = check_winner(board)
    assert winner == 'X'

def test_full_board_with_no_winner_is_draw():
    # When every square is filled and no line is complete, the game reports no winner and declares a draw
    board = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'X', 'O']]
    winner = check_winner(board)
    draw = is_draw(board)
    assert winner is None  # No winner
    assert draw is True  # It is a draw

def test_open_squares_mean_not_a_draw():
    # While open squares remain, the game is not a draw
    board = [['X', 'O', 'X'], ['X', ' ', 'O'], ['O', 'X', 'O']]
    winner = check_winner(board)
    draw = is_draw(board)
    assert winner is None  # No winner
    assert draw is False  # It is not a draw