from solution import DartsGame

def test_start_of_game():
    game = DartsGame()
    assert game.score == 301  # AC-1.1: A new game has a score of 301
    assert game.turn == 1  # AC-1.2: A new game is on turn 1
    assert game.darts_remaining == 3  # AC-1.2: With 3 darts available
    assert not game.is_finished()  # AC-1.2: The game is not finished


def test_plain_dart_scoring():
    game = DartsGame()
    game.throw(20)  # AC-2.1: Throw a plain dart
    assert game.score == 281  # 301 - 20 = 281


def test_double_scoring():
    game = DartsGame()
    game.throw('double', 20)  # AC-2.2: Throw a double dart
    assert game.score == 261  # 301 - (2 * 20) = 261


def test_triple_scoring():
    game = DartsGame()
    game.throw('triple', 20)  # AC-2.3: Throw a triple dart
    assert game.score == 241  # 301 - (3 * 20) = 241


def test_turn_of_three_darts():
    game = DartsGame()
    game.throw(20)
    assert game.darts_remaining == 2  # After first throw
    game.throw(15)
    assert game.darts_remaining == 1  # After second throw
    game.throw(10)  # Third throw ends the turn
    assert game.turn == 2  # The game reports the next turn number
    assert game.darts_remaining == 3  # With 3 darts available again


def test_bust_exactly_one():
    game = DartsGame()
    game.throw(20)  # First throw
    game.throw(20)  # Second throw
    game.throw(20)  # Third throw, score becomes 241
    assert game.score == 241  # Score after normal throws
    game.throw(20)  # AC-4.1: Throw that leaves score of exactly 1
    assert game.score == 241  # Score should remain at the start of turn
    assert game.darts_remaining == 3  # Turn ends immediately
    assert not game.is_finished()  # Game should remain unfinished


def test_bust_below_zero():
    game = DartsGame()
    game.throw(5)  # First throw
    game.throw(10)  # Second throw
    game.throw(16)  # AC-4.2: Throw that takes score below zero (score goes from 286 to 270)
    assert game.score == 286  # Score should remain at the start of turn
    assert game.darts_remaining == 3  # Turn ends immediately
    assert not game.is_finished()  # Game should remain unfinished


def test_bust_without_double():
    game = DartsGame()
    game.throw(20)  # First throw
    game.throw(20)  # Second throw
    game.throw(20)  # Third throw, score becomes 241
    game.throw(241)  # AC-4.3: Throw that reaches exactly zero without a double
    assert game.score == 241  # Score should remain at 241
    assert game.darts_remaining == 3  # Turn ends immediately
    assert not game.is_finished()  # Game should remain unfinished


def test_bust_on_final_dart():
    game = DartsGame()
    game.throw(20)  # First throw
    game.throw(20)  # Second throw
    game.throw(20)  # Third throw, score becomes 241
    game.throw(25)  # AC-4.4: Throw that is a bust
    assert game.score == 241  # Score should remain at 241
    assert game.darts_remaining == 3  # Turn ends immediately
    assert not game.is_finished()  # Game should remain unfinished


def test_winning_with_double():
    game = DartsGame()
    game.throw('triple', 20)  # First throw, score goes to 221 (301 - 60)
    game.throw('triple', 7)    # Second throw, score goes to 200 (221 - 21)
    game.throw('double', 20)    # AC-5.1: Winning throw with a double
    assert game.score == 0  # Game should end with score at zero
    assert game.is_finished()  # Game should be finished