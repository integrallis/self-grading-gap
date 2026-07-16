# test_darts.py

from solution import DartsGame

def test_start_of_game():
    game = DartsGame()
    assert game.score == 301  # AC-1.1: A new game has a score of 301
    assert game.finished is False  # AC-1.1: The game is not finished
    assert game.turn == 1  # AC-1.2: The game is on turn 1
    assert game.darts_remaining == 3  # AC-1.2: 3 darts available

def test_plain_dart_subtraction():
    game = DartsGame()
    game.throw_dart(20)  # AC-2.1: Throwing a plain dart with value 20
    assert game.score == 281  # 301 - 20 = 281

def test_double_dart_subtraction():
    game = DartsGame()
    game.throw_dart(20, is_double=True)  # AC-2.2: Throwing a double dart with value 20
    assert game.score == 261  # 301 - (2 * 20) = 261

def test_triple_dart_subtraction():
    game = DartsGame()
    game.throw_dart(20, is_triple=True)  # AC-2.3: Throwing a triple dart with value 20
    assert game.score == 241  # 301 - (3 * 20) = 241

def test_turns_of_three_darts():
    game = DartsGame()
    game.throw_dart(20)
    assert game.darts_remaining == 2  # AC-3.1: Darts remaining after first throw
    game.throw_dart(20)
    assert game.darts_remaining == 1  # AC-3.1: Darts remaining after second throw
    game.throw_dart(20)
    assert game.darts_remaining == 3  # AC-3.1: Third throw ends the turn, reset darts
    assert game.turn == 2  # AC-3.1: Next turn number is 2

def test_bust_exactly_one():
    game = DartsGame()
    game.throw_dart(20)  # Start turn
    game.throw_dart(20)  # 301 - 20 = 281
    game.throw_dart(300)  # AC-4.1: Throwing a dart that leaves exactly 1
    assert game.score == 301  # Score should revert to 301
    assert game.finished is False  # Game is still unfinished
    assert game.turn == 2  # Turn should increment to 2
    assert game.darts_remaining == 3  # Darts reset

def test_bust_below_zero():
    game = DartsGame()
    game.throw_dart(20)  # Start turn
    game.throw_dart(400)  # AC-4.2: Throwing a dart that takes score below zero
    assert game.score == 301  # Score should revert to 301
    assert game.finished is False  # Game is still unfinished

def test_bust_without_double():
    game = DartsGame()
    game.throw_dart(20)  # Start turn
    game.throw_dart(300)  # 301 - 20 = 281
    game.throw_dart(281)  # AC-4.3: Throwing a dart that reaches exactly zero without a double
    assert game.score == 301  # Score should revert to 301
    assert game.finished is False  # Game is still unfinished
    assert game.turn == 2  # Turn should increment to 2
    assert game.darts_remaining == 3  # Darts reset

def test_bust_restores_score():
    game = DartsGame()
    game.throw_dart(20)  # Start turn
    game.throw_dart(300)  # Bust with a dart that goes below zero
    assert game.score == 301  # Score should revert to 301
    assert game.turn == 2  # Turn should increment to 2
    assert game.darts_remaining == 3  # Darts reset

def test_win_with_double():
    game = DartsGame()
    game.throw_dart(20)  # Reduce score to 281
    game.throw_dart(20)  # Reduce score to 261
    game.throw_dart(20, is_triple=True)  # Reduce score to 201 (triple 20)
    game.throw_dart(20, is_triple=True)  # Reduce score to 141 (triple 20)
    game.throw_dart(20, is_double=True)  # AC-5.1: Throwing a double to reach exactly zero
    assert game.score == 0  # Game should be won
    assert game.finished is True  # Game should be finished