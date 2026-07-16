# test_darts.py

from solution import DartsGame

def test_new_game_starts_at_301():
    game = DartsGame()
    assert game.score == 301  # AC-1.1: New game has a score of 301
    assert not game.finished  # AC-1.1: Game is not finished
    assert game.turn == 1  # AC-1.2: Game is on turn 1
    assert game.darts_remaining == 3  # AC-1.2: 3 darts available

def test_plain_dart_scoring():
    game = DartsGame()
    game.throw_dart(20)  # AC-2.1: Throw a plain dart with value 20
    assert game.score == 281  # 301 - 20 = 281

def test_double_dart_scoring():
    game = DartsGame()
    game.throw_dart(10, double=True)  # AC-2.2: Throw a double dart with value 10
    assert game.score == 281  # 301 - 20 = 281

def test_triple_dart_scoring():
    game = DartsGame()
    game.throw_dart(5, triple=True)  # AC-2.3: Throw a triple dart with value 5
    assert game.score == 286  # 301 - 15 = 286

def test_turns_of_three_darts():
    game = DartsGame()
    game.throw_dart(20)
    game.throw_dart(15)
    game.throw_dart(10)  # AC-3.1: Third dart ends the turn
    assert game.turn == 2  # New turn number
    assert game.darts_remaining == 3  # 3 darts available again

def test_bust_leaves_one():
    game = DartsGame()
    game.throw_dart(20)  # Score is now 281
    game.throw_dart(100)  # Score is now 181
    game.throw_dart(180)  # AC-4.1: Bust, score cannot go below 0
    assert game.score == 281  # Score restored to the start of the turn
    assert game.turn == 2  # Turn has not advanced
    assert game.darts_remaining == 3  # Darts remaining reset

def test_bust_leaves_score_below_zero():
    game = DartsGame()
    game.throw_dart(20)  # Score is now 281
    game.throw_dart(100)  # Score is now 181
    game.throw_dart(200)  # AC-4.2: Bust, score cannot go below 0
    assert game.score == 281  # Score restored to the start of the turn
    assert game.turn == 2  # Turn has not advanced
    assert game.darts_remaining == 3  # Darts remaining reset

def test_bust_reaches_zero_without_double():
    game = DartsGame()
    game.throw_dart(20)  # Score is now 281
    game.throw_dart(100)  # Score is now 181
    game.throw_dart(181)  # AC-4.3: Bust, score reaches 0 without a double
    assert game.score == 281  # Score restored to the start of the turn
    assert game.turn == 2  # Turn has not advanced
    assert game.darts_remaining == 3  # Darts remaining reset

def test_winning_with_double():
    game = DartsGame()
    game.throw_dart(20)  # Score is now 281
    game.throw_dart(20)  # Score is now 261
    game.throw_dart(1, double=True)  # AC-5.1: Winning move, reach exactly 0 with a double
    assert game.finished  # Game is finished
    assert game.score == 0  # Score is exactly 0