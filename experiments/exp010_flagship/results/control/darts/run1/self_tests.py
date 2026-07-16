from solution import start_game, throw_dart

def test_start_game():
    game = start_game()
    # A new game should start with a score of 301 and be unfinished
    assert game['score'] == 301  # AC-1.1
    assert not game['finished']    # AC-1.1
    assert game['turn'] == 1       # AC-1.2
    assert game['darts_remaining'] == 3  # AC-1.2

def test_plain_dart_scoring():
    game = start_game()
    game = throw_dart(game, 20)
    # 301 - 20 = 281
    assert game['score'] == 281  # AC-2.1

def test_double_dart_scoring():
    game = start_game()
    game = throw_dart(game, 'double', 20)
    # 301 - (2 * 20) = 261
    assert game['score'] == 261  # AC-2.2

def test_triple_dart_scoring():
    game = start_game()
    game = throw_dart(game, 'triple', 20)
    # 301 - (3 * 20) = 241
    assert game['score'] == 241  # AC-2.3

def test_turns_of_three_darts():
    game = start_game()
    game = throw_dart(game, 20)  # 301 - 20 = 281
    game = throw_dart(game, 20)  # 281 - 20 = 261
    game = throw_dart(game, 20)  # 261 - 20 = 241
    # After three darts, the turn ends and the next turn should start
    assert game['turn'] == 2  # AC-3.1
    assert game['darts_remaining'] == 3  # AC-3.1

def test_bust_exactly_one():
    game = start_game()
    game = throw_dart(game, 300)  # 301 - 300 = 1
    # A bust should restore the score to the start of the turn (301)
    assert game['score'] == 301  # AC-4.1
    assert game['finished'] == False  # AC-4.1
    assert game['turn'] == 1  # AC-4.1
    assert game['darts_remaining'] == 3  # AC-4.1

def test_bust_below_zero():
    game = start_game()
    game = throw_dart(game, 200)  # 301 - 200 = 101
    game = throw_dart(game, 100)  # 101 - 100 = 1
    game = throw_dart(game, 2)  # 1 - 2 = -1 (bust)
    # A bust should restore the score to the start of the turn (301)
    assert game['score'] == 301  # AC-4.2
    assert game['finished'] == False  # AC-4.2
    assert game['turn'] == 1  # AC-4.2
    assert game['darts_remaining'] == 3  # AC-4.2

def test_bust_zero_without_double():
    game = start_game()
    game = throw_dart(game, 299)  # 301 - 299 = 2
    game = throw_dart(game, 2)  # 2 - 2 = 0 (not a double)
    # A bust should restore the score to the start of the turn (301)
    assert game['score'] == 301  # AC-4.3
    assert game['finished'] == False  # AC-4.3
    assert game['turn'] == 1  # AC-4.3
    assert game['darts_remaining'] == 3  # AC-4.3

def test_win_with_double():
    game = start_game()
    game = throw_dart(game, 300)  # 301 - 300 = 1
    game = throw_dart(game, 'double', 1)  # 1 - (2 * 1) = 0 (win)
    # The game should be finished upon winning
    assert game['score'] == 0  # AC-5.1
    assert game['finished'] == True  # AC-5.1