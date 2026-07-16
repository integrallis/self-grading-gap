# test_tic_tac_toe.py

from solution import TicTacToe

def test_start_fresh_game():
    game = TicTacToe()
    # AC-1.1: A new game presents a three-by-three board of blank squares
    expected_board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert game.board == expected_board
    
    # AC-1.2: X is the first player to move
    assert game.current_player == 'X'

def test_take_turns_marking_squares():
    game = TicTacToe()
    
    # AC-2.1: A move marks the chosen square
    game.make_move(0, 0)  # X moves
    assert game.board[0][0] == 'X'
    
    # AC-2.2: After each move the turn passes to the other player
    assert game.current_player == 'O'
    
    game.make_move(1, 1)  # O moves
    assert game.board[1][1] == 'O'
    assert game.current_player == 'X'
    
    # Test asymmetric coordinates to verify correct marking
    game.make_move(0, 2)  # X moves
    assert game.board[0][2] == 'X'  # Ensure (0, 2) is marked correctly
    assert game.current_player == 'O'

def test_win_with_three_in_a_line():
    game = TicTacToe()
    
    # X makes a winning move across the first row
    game.make_move(0, 0)  # X
    game.make_move(1, 0)  # O
    game.make_move(0, 1)  # X
    game.make_move(1, 1)  # O
    game.make_move(0, 2)  # X wins
    assert game.check_winner() == 'X'  # AC-3.1
    
    game = TicTacToe()  # Reset for next test
    
    # O makes a winning move across the second row
    game.make_move(0, 0)  # X
    game.make_move(0, 1)  # O
    game.make_move(1, 0)  # X
    game.make_move(1, 1)  # O
    game.make_move(1, 2)  # O wins
    assert game.check_winner() == 'O'  # AC-3.1
    
    game = TicTacToe()  # Reset for next test
    
    # X makes a winning move down the first column
    game.make_move(0, 0)  # X
    game.make_move(0, 1)  # O
    game.make_move(1, 0)  # X
    game.make_move(1, 1)  # O
    game.make_move(2, 0)  # X wins
    assert game.check_winner() == 'X'  # AC-3.2
    
    game = TicTacToe()  # Reset for next test
    
    # O makes a winning move down the second column
    game.make_move(0, 0)  # X
    game.make_move(0, 1)  # O
    game.make_move(1, 0)  # X
    game.make_move(1, 1)  # O
    game.make_move(2, 1)  # O wins
    assert game.check_winner() == 'O'  # AC-3.2
    
    game = TicTacToe()  # Reset for next test
    
    # X makes a winning move along the main diagonal
    game.make_move(0, 0)  # X
    game.make_move(0, 1)  # O
    game.make_move(1, 1)  # X
    game.make_move(1, 0)  # O
    game.make_move(2, 2)  # X wins
    assert game.check_winner() == 'X'  # AC-3.3
    
    game = TicTacToe()  # Reset for next test
    
    # O makes a winning move along the anti-diagonal
    game.make_move(0, 2)  # X
    game.make_move(1, 1)  # O
    game.make_move(2, 0)  # X
    game.make_move(0, 1)  # O
    game.make_move(2, 1)  # O wins
    assert game.check_winner() == 'O'  # AC-3.3
    
    game = TicTacToe()  # Reset for next test
    
    # O makes a winning move along the anti-diagonal with a different completing move
    game.make_move(0, 0)  # X
    game.make_move(0, 2)  # O
    game.make_move(1, 1)  # X
    game.make_move(1, 0)  # O
    game.make_move(2, 0)  # X
    game.make_move(2, 2)  # O wins
    assert game.check_winner() == 'O'  # AC-3.3

def test_end_stalemates_as_draws():
    game = TicTacToe()
    
    # Fill the board without a winner
    moves = [
        (0, 0), (0, 1), (0, 2), 
        (1, 1), (1, 0), (1, 2), 
        (2, 1), (2, 0), (2, 2)
    ]
    for row, col in moves:
        game.make_move(row, col)
    
    assert game.check_winner() is None  # AC-4.1
    assert game.is_draw() is True  # AC-4.1
    
    game = TicTacToe()  # Reset for next test
    
    # Test with open squares remaining
    game.make_move(0, 0)  # X
    game.make_move(0, 1)  # O
    game.make_move(0, 2)  # X
    assert game.is_draw() is False  # AC-4.2