from solution import DartsGame

def test_new_game_start():
    game = DartsGame()
    assert game.score == 301  # AC-1.1: Start score is 301
    assert not game.finished  # AC-1.1: Game is not finished
    assert game.turn == 1  # AC-1.2: Start at turn 1
    assert game.darts_remaining == 3  # AC-1.2: 3 darts available

def test_plain_dart_score():
    game = DartsGame()
    game.throw(20)  # Throw a dart with face value 20
    assert game.score == 281  # AC-2.1: 301 - 20 = 281

def test_double_dart_score():
    game = DartsGame()
    game.throw(20, double=True)  # Throw a double dart with face value 20
    assert game.score == 261  # AC-2.2: 301 - (2 * 20) = 261

def test_triple_dart_score():
    game = DartsGame()
    game.throw(20, triple=True)  # Throw a triple dart with face value 20
    assert game.score == 241  # AC-2.3: 301 - (3 * 20) = 241

def test_turns_of_three_darts():
    game = DartsGame()
    game.throw(20)
    assert game.darts_remaining == 2  # After first throw, 2 darts remaining
    game.throw(20)
    assert game.darts_remaining == 1  # After second throw, 1 dart remaining
    game.throw(20)  # Third dart ends the turn
    assert game.turn == 2  # AC-3.1: Next turn number is 2
    assert game.darts_remaining == 3  # AC-3.1: 3 darts available for the next turn

def test_bust_exactly_one():
    game = DartsGame()
    game.throw(300)  # First throw leaves score at 1
    assert game.score == 301  # AC-4.1: Score restored to 301
    assert not game.finished  # AC-4.4: Game is not finished
    # Turn number after bust is unspecified, so we do not check it
    assert game.darts_remaining == 3  # Darts should reset to 3 after bust

def test_bust_exactly_one_third_dart():
    game = DartsGame()
    game.throw(100)  # First throw leaves score at 201
    game.throw(100)  # Second throw leaves score at 101
    game.throw(1)  # Third dart leaves score at 1
    assert game.score == 301  # AC-4.1: Score restored to 301
    assert not game.finished  # AC-4.4: Game is not finished
    # Turn number after bust is unspecified, so we do not check it
    assert game.darts_remaining == 3  # Darts should reset to 3 after bust

def test_bust_below_zero():
    game = DartsGame()
    game.throw(250)  # First throw (assumed bust)
    game.throw(60)  # Second throw leaves score at -9
    assert game.score == 301  # AC-4.2: Score restored to 301
    assert not game.finished  # AC-4.4: Game is not finished
    # Turn number after bust is unspecified, so we do not check it
    assert game.darts_remaining == 3  # Darts should reset to 3 after bust

def test_bust_reach_zero_without_double():
    game = DartsGame()
    game.throw(200)  # First throw leaves score at 101
    game.throw(100)  # Second throw leaves score at 1
    assert game.score == 301  # AC-4.3: Score restored to 301
    assert not game.finished  # AC-4.4: Game is not finished
    # Turn number after bust is unspecified, so we do not check it
    assert game.darts_remaining == 3  # Darts should reset to 3 after bust

def test_win_with_double():
    game = DartsGame()
    game.throw(20)  # First throw leaves score at 281
    game.throw(1)  # Second throw leaves score at 280
    game.throw(2, double=True)  # Third throw, double 2 wins
    assert game.score == 0  # AC-5.1: Score is 0
    assert game.finished  # AC-5.1: Game is finished