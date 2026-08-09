from solution import start_game, make_move, check_winner, is_draw

def test_start_game_creates_empty_board():
    # Expected: 3 rows of 3 spaces each
    expected_board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    game_state = start_game()
    assert game_state['board'] == expected_board

def test_start_game_first_player_is_X():
    # Expected: First player is 'X'
    game_state = start_game()
    assert game_state['current_player'] == 'X'

def test_make_move_marks_square_correctly():
    # Start a game and make a move
    game_state = start_game()
    make_move(game_state, 0, 0)  # X makes a move at (0, 0)
    expected_board = [["X", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    assert game_state['board'] == expected_board

def test_make_move_passes_turn_to_O():
    # Start a game and make a move
    game_state = start_game()
    make_move(game_state, 0, 0)  # X moves
    assert game_state['current_player'] == 'O'  # Next turn should be O

def test_make_move_marks_square_correctly_at_different_position():
    # Start a game and make a move at (0, 2)
    game_state = start_game()
    make_move(game_state, 0, 2)  # X makes a move at (0, 2)
    expected_board = [[" ", " ", "X"], [" ", " ", " "], [" ", " ", " "]]
    assert game_state['board'] == expected_board

def test_make_move_records_O_mark_and_passes_turn_back_to_X():
    # Start a game and make a move for O
    game_state = start_game()
    make_move(game_state, 0, 0)  # X moves
    make_move(game_state, 1, 1)  # O moves
    expected_board = [["X", " ", " "], [" ", "O", " "], [" ", " ", " "]]
    assert game_state['board'] == expected_board
    assert game_state['current_player'] == 'X'  # Next turn should be X

def test_three_in_a_row_wins_game():
    # X makes a winning move
    game_state = start_game()
    make_move(game_state, 0, 0)  # X
    make_move(game_state, 1, 0)  # O
    make_move(game_state, 0, 1)  # X
    make_move(game_state, 1, 1)  # O
    make_move(game_state, 0, 2)  # X wins
    assert check_winner(game_state) == 'X'  # X should be the winner

def test_three_in_a_column_wins_game():
    # X makes a winning move
    game_state = start_game()
    make_move(game_state, 0, 0)  # X
    make_move(game_state, 0, 1)  # O
    make_move(game_state, 1, 0)  # X
    make_move(game_state, 1, 1)  # O
    make_move(game_state, 2, 0)  # X wins
    assert check_winner(game_state) == 'X'  # X should be the winner

def test_three_in_a_diagonal_wins_game():
    # X makes a winning move diagonally
    game_state = start_game()
    make_move(game_state, 0, 0)  # X
    make_move(game_state, 0, 1)  # O
    make_move(game_state, 1, 1)  # X
    make_move(game_state, 0, 2)  # O
    make_move(game_state, 2, 2)  # X wins
    assert check_winner(game_state) == 'X'  # X should be the winner

def test_three_in_a_anti_diagonal_wins_game():
    # X makes a winning move in the anti-diagonal
    game_state = start_game()
    make_move(game_state, 0, 2)  # X
    make_move(game_state, 0, 1)  # O
    make_move(game_state, 1, 1)  # X
    make_move(game_state, 1, 0)  # O
    make_move(game_state, 2, 0)  # X wins
    assert check_winner(game_state) == 'X'  # X should be the winner

def test_O_wins_game():
    # O makes a winning move
    game_state = start_game()
    make_move(game_state, 0, 0)  # X
    make_move(game_state, 0, 1)  # O
    make_move(game_state, 1, 0)  # X
    make_move(game_state, 1, 1)  # O
    make_move(game_state, 2, 1)  # X
    make_move(game_state, 2, 2)  # O wins
    assert check_winner(game_state) is None  # No winner

def test_is_draw_when_board_full_no_winner():
    # Fill the board with no winner
    game_state = start_game()
    moves = [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 1), (2, 0), (2, 2)
    ]
    players = ['X', 'O'] * 4  # Alternating moves
    for i, (row, col) in enumerate(moves):
        make_move(game_state, row, col)  # Fill the board
    assert check_winner(game_state) is None  # No winner
    assert is_draw(game_state)  # Should be a draw

def test_not_draw_when_squares_open():
    # Start a game and make a move
    game_state = start_game()
    make_move(game_state, 0, 0)  # X makes a move
    assert not is_draw(game_state)  # Should not be a draw

def test_diagonal_win_with_any_last_square():
    # Test diagonal win with different last moves
    for last_move in [(0, 0), (1, 1), (2, 2)]:
        game_state = start_game()
        make_move(game_state, 0, 0)  # X
        make_move(game_state, 0, 1)  # O
        make_move(game_state, 1, 1)  # X
        make_move(game_state, 0, 2)  # O
        make_move(game_state, *last_move)  # X wins with diagonal
        assert check_winner(game_state) == 'X'  # X should be the winner