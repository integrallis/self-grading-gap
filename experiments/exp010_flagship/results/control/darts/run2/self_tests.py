from solution import start_game, throw_dart

def test_start_game():
    game = start_game()
    # AC-1.1: A new game has a score of 301
    assert game['score'] == 301
    # AC-1.2: A new game is on turn 1 with 3 darts available
    assert game['turn'] == 1
    assert game['darts_remaining'] == 3
    assert not game['finished']

def test_plain_dart_scoring():
    game = start_game()
    game = throw_dart(game, 20)  # AC-2.1: 301 - 20
    assert game['score'] == 281

def test_double_dart_scoring():
    game = start_game()
    game = throw_dart(game, 20, is_double=True)  # AC-2.2: 301 - (2 * 20)
    assert game['score'] == 261

def test_triple_dart_scoring():
    game = start_game()
    game = throw_dart(game, 20, is_triple=True)  # AC-2.3: 301 - (3 * 20)
    assert game['score'] == 221

def test_turn_of_three_darts():
    game = start_game()
    game = throw_dart(game, 20)
    game = throw_dart(game, 10)
    game = throw_dart(game, 5)  # AC-3.1: After 3 darts, turn ends

    assert game['turn'] == 2  # next turn number
    assert game['darts_remaining'] == 3

def test_bust_exactly_one():
    game = start_game()
    game = throw_dart(game, 300)  # going to leave 1
    game = throw_dart(game, 1)    # AC-4.1: bust on last dart
    assert game['score'] == 301  # score restored to start of turn
    assert game['darts_remaining'] == 3  # turn ends immediately
    assert not game['finished']

def test_bust_below_zero():
    game = start_game()
    game = throw_dart(game, 300)  # going to leave 1
    game = throw_dart(game, 2)    # AC-4.2: bust
    assert game['score'] == 301  # score restored to start of turn
    assert game['darts_remaining'] == 3  # turn ends immediately
    assert not game['finished']

def test_bust_not_double():
    game = start_game()
    game = throw_dart(game, 300)  # going to leave 1
    game = throw_dart(game, 0, is_double=True)  # AC-4.3: reaches zero but not double
    assert game['score'] == 301  # score restored to start of turn
    assert game['darts_remaining'] == 3  # turn ends immediately
    assert not game['finished']

def test_win_with_double():
    game = start_game()
    game = throw_dart(game, 300)  # going to leave 1
    game = throw_dart(game, 1, is_double=True)  # AC-5.1: win with double
    assert game['score'] == 0  # score is 0
    assert game['finished']  # game is finished