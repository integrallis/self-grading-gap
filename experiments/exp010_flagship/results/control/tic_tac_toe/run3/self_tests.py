# test_tic_tac_toe.py

from solution import start_game, make_move, check_winner, is_draw

def test_start_game_creates_blank_board():
    # A new game should present a 3x3 board of blank squares
    expected_board = [[' ', ' ', ' '], 
                      [' ', ' ', ' '], 
                      [' ', ' ', ' ']]
    assert start_game() == expected_board

def test_start_game_first_player_is_x():
    # X is the first player to move
    game = start_game()
    assert game['current_player'] == 'X'

def test_make_move_marks_square():
    game = start_game()
    make_move(game, 0, 0)  # X moves
    expected_board = [['X', ' ', ' '], 
                      [' ', ' ', ' '], 
                      [' ', ' ', ' ']]
    assert game['board'] == expected_board

def test_make_move_alternates_turns():
    game = start_game()
    make_move(game, 0, 0)  # X moves
    assert game['current_player'] == 'O'
    make_move(game, 1, 1)  # O moves
    assert game['current_player'] == 'X'

def test_win_row():
    game = start_game()
    make_move(game, 0, 0)  # X moves
    make_move(game, 1, 0)  # O moves
    make_move(game, 0, 1)  # X moves
    make_move(game, 1, 1)  # O moves
    make_move(game, 0, 2)  # X moves
    assert check_winner(game) == 'X'  # X wins with a row

def test_win_column():
    game = start_game()
    make_move(game, 0, 0)  # X moves
    make_move(game, 0, 1)  # O moves
    make_move(game, 1, 0)  # X moves
    make_move(game, 1, 1)  # O moves
    make_move(game, 2, 0)  # X moves
    assert check_winner(game) == 'X'  # X wins with a column

def test_win_diagonal():
    game = start_game()
    make_move(game, 0, 0)  # X moves
    make_move(game, 0, 1)  # O moves
    make_move(game, 1, 1)  # X moves
    make_move(game, 1, 0)  # O moves
    make_move(game, 2, 2)  # X moves
    assert check_winner(game) == 'X'  # X wins with a diagonal

def test_draw_full_board_no_winner():
    game = start_game()
    moves = [(0, 0), (0, 1), (0, 2),
             (1, 0), (1, 1), (1, 2),
             (2, 0), (2, 2), (2, 1)]
    for i, (row, col) in enumerate(moves):
        make_move(game, row, col)
    assert is_draw(game) == True  # Full board with no winner

def test_not_draw_with_open_squares():
    game = start_game()
    make_move(game, 0, 0)
    make_move(game, 0, 1)
    assert is_draw(game) == False  # Open squares remain