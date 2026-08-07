# test_tic_tac_toe.py

from solution import start_game, make_move, check_winner, check_draw

def test_start_game_creates_empty_board():
    # AC-1.1: A new game presents a three-by-three board of blank squares
    expected_board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    game = start_game()
    assert game['board'] == expected_board

def test_start_game_sets_first_player_to_x():
    # AC-1.2: X is the first player to move
    game = start_game()
    assert game['current_player'] == 'X'

def test_make_move_marks_square_for_x():
    # AC-2.1: A move marks the chosen square with the letter of the player whose turn it is
    game = start_game()
    make_move(game, 0, 0)  # X moves
    expected_board = [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert game['board'] == expected_board

def test_make_move_marks_square_for_o():
    # AC-2.1: A move marks the chosen square with the letter of the player whose turn it is
    game = start_game()
    make_move(game, 0, 0)  # X moves
    make_move(game, 1, 1)  # O moves
    expected_board = [['X', ' ', ' '], [' ', 'O', ' '], [' ', ' ', ' ']]
    assert game['board'] == expected_board

def test_make_move_alternates_turns():
    # AC-2.2: After each move the turn passes to the other player
    game = start_game()
    make_move(game, 0, 0)  # X moves
    assert game['current_player'] == 'O'
    make_move(game, 1, 1)  # O moves
    assert game['current_player'] == 'X'

def test_make_move_non_symmetric_coordinates():
    # AC-2.1: A move marks the chosen square with the letter of the player whose turn it is
    game = start_game()
    make_move(game, 0, 2)  # X moves to top-right
    expected_board = [[' ', ' ', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert game['board'] == expected_board

def test_check_winner_row_middle():
    # AC-3.1: Three matching marks across a row win the game for that player
    game = start_game()
    make_move(game, 1, 0)  # X moves
    make_move(game, 1, 1)  # O moves
    make_move(game, 1, 2)  # X moves
    assert check_winner(game) == 'X'
    
def test_check_winner_row_bottom():
    # AC-3.1: Three matching marks across a row win the game for that player
    game = start_game()
    make_move(game, 2, 0)  # X moves
    make_move(game, 2, 1)  # O moves
    make_move(game, 2, 2)  # X moves
    assert check_winner(game) == 'X'

def test_check_winner_column_middle():
    # AC-3.2: Three matching marks down a column win the game for that player
    game = start_game()
    make_move(game, 0, 1)  # X moves
    make_move(game, 1, 1)  # O moves
    make_move(game, 2, 1)  # X moves
    assert check_winner(game) == 'X'
    
def test_check_winner_column_right():
    # AC-3.2: Three matching marks down a column win the game for that player
    game = start_game()
    make_move(game, 0, 2)  # X moves
    make_move(game, 1, 2)  # O moves
    make_move(game, 2, 2)  # X moves
    assert check_winner(game) == 'X'

def test_check_winner_diagonal():
    # AC-3.3: Three matching marks along either diagonal win the game
    game = start_game()
    make_move(game, 0, 0)  # X moves
    make_move(game, 1, 1)  # O moves
    make_move(game, 2, 2)  # X moves
    assert check_winner(game) == 'X'

def test_check_winner_reverse_diagonal():
    # AC-3.3: Three matching marks along either diagonal win the game
    game = start_game()
    make_move(game, 0, 2)  # X moves
    make_move(game, 1, 1)  # O moves
    make_move(game, 2, 0)  # X moves
    assert check_winner(game) == 'X'

def test_check_winner_o_in_row():
    # Check winner for O in a row
    game = start_game()
    make_move(game, 0, 0)  # O moves
    make_move(game, 0, 1)  # X moves
    make_move(game, 0, 2)  # O moves
    assert check_winner(game) == 'O'

def test_check_draw_when_full_no_winner():
    # AC-4.1: When every square is filled and no line is complete, the game reports no winner and declares a draw
    game = start_game()
    make_move(game, 0, 0)  # X moves
    make_move(game, 0, 1)  # O moves
    make_move(game, 0, 2)  # X moves
    make_move(game, 1, 0)  # O moves
    make_move(game, 1, 1)  # X moves
    make_move(game, 1, 2)  # O moves
    make_move(game, 2, 0)  # X moves
    make_move(game, 2, 1)  # O moves
    make_move(game, 2, 2)  # X moves
    assert check_winner(game) is None  # No winner
    assert check_draw(game) == True

def test_check_not_draw_with_open_squares():
    # AC-4.2: While open squares remain, the game is not a draw
    game = start_game()
    make_move(game, 0, 0)  # X moves
    make_move(game, 0, 1)  # O moves
    make_move(game, 0, 2)  # X moves
    make_move(game, 1, 0)  # O moves
    make_move(game, 1, 1)  # X moves
    assert check_draw(game) == False  # There are still open squares