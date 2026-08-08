from solution import start_game, make_move, check_winner, is_draw

def test_start_game_creates_empty_board():
    # AC-1.1: A new game presents a three-by-three board of blank squares
    board = start_game()
    expected_board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    # Check that the board has 3 rows and each row has 3 spaces
    assert board == expected_board  # Checking the expected structure of the board

def test_start_game_sets_first_player():
    # AC-1.2: X is the first player to move.
    board, current_player = start_game()
    assert current_player == 'X'  # Check that the first player is 'X'

def test_make_move_marks_square():
    # AC-2.1: A move marks the chosen square with the letter of the player
    board, current_player = start_game()
    board = make_move(board, 0, 0, current_player)  # X marks (0, 0)
    expected_board = [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert board == expected_board  # Check that the board is updated correctly

def test_make_move_alternates_players():
    # AC-2.2: After each move the turn passes to the other player
    board, current_player = start_game()
    board = make_move(board, 0, 0, current_player)  # X marks (0, 0)
    board, current_player = make_move(board, 0, 1, current_player)  # O marks (0, 1)
    assert board[0][1] == 'O'  # Check that O has marked the position
    assert board[0][0] == 'X'  # Ensure previous move is still there

def test_check_winner_row():
    # AC-3.1: Three matching marks across a row win the game
    board = [['X', 'X', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']]
    winner = check_winner(board)
    assert winner == 'X'  # Check that X is the winner

def test_check_winner_column():
    # AC-3.2: Three matching marks down a column win the game
    board = [['X', ' ', ' '], ['X', ' ', ' '], ['X', ' ', ' ']]
    winner = check_winner(board)
    assert winner == 'X'  # Check that X is the winner

def test_check_winner_diagonal():
    # AC-3.3: Three matching marks along either diagonal win the game
    board = [['X', ' ', 'O'], [' ', 'X', ' '], ['O', ' ', 'X']]
    winner = check_winner(board)
    assert winner == 'X'  # Check that X is the winner

def test_check_winner_row_O():
    # Check that O wins in the bottom row
    board = [[' ', ' ', ' '], [' ', ' ', ' '], ['O', 'O', 'O']]
    winner = check_winner(board)
    assert winner == 'O'  # Check that O is the winner

def test_check_winner_column_O():
    # Check that O wins in the middle column
    board = [[' ', 'O', ' '], [' ', 'O', ' '], [' ', 'O', ' ']]
    winner = check_winner(board)
    assert winner == 'O'  # Check that O is the winner

def test_check_winner_anti_diagonal():
    # Check anti-diagonal win
    board = [['O', ' ', 'X'], [' ', 'O', ' '], ['X', ' ', 'O']]
    winner = check_winner(board)
    assert winner == 'O'  # Check that O is the winner

def test_check_winner_non_top_row():
    # Check a win in the middle row
    board = [[' ', ' ', ' '], ['X', 'X', 'X'], [' ', ' ', ' ']]
    winner = check_winner(board)
    assert winner == 'X'  # Check that X is the winner

def test_check_winner_non_left_column():
    # Check a win in the right column
    board = [[' ', ' ', 'X'], [' ', ' ', 'X'], [' ', ' ', 'X']]
    winner = check_winner(board)
    assert winner == 'X'  # Check that X is the winner

def test_check_no_winner():
    # No matching marks in any row, column or diagonal
    board = [['X', 'O', 'X'], ['X', 'O', 'O'], ['O', 'X', 'X']]
    winner = check_winner(board)
    assert winner is None  # Check that there is no winner

def test_is_draw_full_board_no_winner():
    # AC-4.1: When every square is filled and no line is complete, it's a draw
    board = [['X', 'O', 'X'], ['X', 'O', 'O'], ['O', 'X', 'X']]
    draw = is_draw(board)
    assert draw is True  # Check that it is a draw

def test_is_draw_not_full():
    # AC-4.2: While open squares remain, the game is not a draw
    board = [['X', 'O', 'X'], ['O', ' ', 'O'], ['O', 'X', 'X']]
    draw = is_draw(board)
    assert draw is False  # Check that it is not a draw