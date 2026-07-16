# test_tic_tac_toe.py

from solution import TicTacToe

def test_start_a_fresh_game():
    game = TicTacToe()
    assert game.current_player == 'X'  # AC-1.2
    # AC-1.1: Check that the board is fresh and has blank squares.
    assert game.board == [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]  # Assuming board is a 3x3 list of lists

def test_take_turns_marking_squares():
    game = TicTacToe()
    game.make_move(0, 0)  # X's turn
    assert game.board == [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]  # AC-2.1
    assert game.current_player == 'O'  # AC-2.2
    
    game.make_move(1, 1)  # O's turn
    assert game.board == [['X', ' ', ' '], [' ', 'O', ' '], [' ', ' ', ' ']]  # AC-2.1
    assert game.current_player == 'X'  # AC-2.2

    game.make_move(0, 2)  # X's turn
    assert game.board == [['X', ' ', 'X'], [' ', 'O', ' '], [' ', ' ', ' ']]  # AC-2.1
    assert game.current_player == 'O'  # AC-2.2

def test_take_turns_marking_squares_row_column_order():
    game = TicTacToe()
    game.make_move(0, 2)  # X's turn
    assert game.board == [[' ', ' ', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']]  # Verify it marks the correct square
    game.make_move(2, 0)  # O's turn
    assert game.board == [[' ', ' ', 'X'], [' ', ' ', ' '], ['O', ' ', ' ']]  # Verify it marks the correct square

def test_win_with_three_in_a_line_rows():
    game = TicTacToe()
    game.make_move(0, 0)  # X
    game.make_move(1, 0)  # O
    game.make_move(0, 1)  # X
    game.make_move(1, 1)  # O
    game.make_move(0, 2)  # X wins
    assert game.winner == 'X'  # AC-3.1

def test_win_with_three_in_a_line_columns():
    game = TicTacToe()
    game.make_move(0, 0)  # X
    game.make_move(0, 1)  # O
    game.make_move(1, 0)  # X
    game.make_move(1, 1)  # O
    game.make_move(2, 0)  # X wins
    assert game.winner == 'X'  # AC-3.2

def test_win_with_three_in_a_line_diagonals():
    game = TicTacToe()
    game.make_move(0, 0)  # X
    game.make_move(0, 1)  # O
    game.make_move(1, 1)  # X
    game.make_move(1, 0)  # O
    game.make_move(2, 2)  # X wins
    assert game.winner == 'X'  # AC-3.3

def test_win_with_other_diagonal():
    game = TicTacToe()
    game.make_move(0, 2)  # X
    game.make_move(0, 0)  # O
    game.make_move(1, 1)  # X
    game.make_move(1, 0)  # O
    game.make_move(2, 0)  # X wins
    assert game.winner == 'X'  # AC-3.3

def test_win_with_middle_row():
    game = TicTacToe()
    game.make_move(1, 0)  # X
    game.make_move(0, 0)  # O
    game.make_move(1, 1)  # X
    game.make_move(0, 1)  # O
    game.make_move(1, 2)  # X wins
    assert game.winner == 'X'  # Test middle row win

def test_win_with_bottom_row():
    game = TicTacToe()
    game.make_move(2, 0)  # X
    game.make_move(0, 0)  # O
    game.make_move(2, 1)  # X
    game.make_move(0, 1)  # O
    game.make_move(2, 2)  # X wins
    assert game.winner == 'X'  # Test bottom row win

def test_win_with_middle_column():
    game = TicTacToe()
    game.make_move(0, 1)  # X
    game.make_move(0, 0)  # O
    game.make_move(1, 1)  # X
    game.make_move(1, 0)  # O
    game.make_move(2, 1)  # X wins
    assert game.winner == 'X'  # Test middle column win

def test_win_with_right_column():
    game = TicTacToe()
    game.make_move(0, 2)  # X
    game.make_move(0, 0)  # O
    game.make_move(1, 2)  # X
    game.make_move(1, 0)  # O
    game.make_move(2, 2)  # X wins
    assert game.winner == 'X'  # Test right column win

def test_win_with_non_bottom_square_diagonal():
    game = TicTacToe()
    game.make_move(0, 0)  # X
    game.make_move(0, 1)  # O
    game.make_move(1, 1)  # X
    game.make_move(1, 2)  # O
    game.make_move(2, 2)  # X wins
    assert game.winner == 'X'  # Test diagonal win with non-bottom square

def test_end_stalemates_as_draw():
    game = TicTacToe()
    moves = [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2)
    ]
    players = ['X', 'O'] * 4  # 4 X's and 4 O's
    for move, player in zip(moves, players):
        game.make_move(*move)  # Assuming make_move checks the current_player
    assert game.winner is None  # AC-4.1
    assert game.is_draw()  # AC-4.1

def test_not_a_draw_with_open_squares():
    game = TicTacToe()
    game.make_move(0, 0)  # X
    game.make_move(0, 1)  # O
    assert not game.is_draw()  # AC-4.2