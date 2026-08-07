import pytest
from solution import Darts301

def test_new_game_starts_at_301():
    game = Darts301()
    assert game.score == 301  # AC-1.1: New game score should be 301
    assert not game.finished  # AC-1.1: Game should not be finished
    assert game.turn == 1  # AC-1.2: Game should be on turn 1
    assert game.darts_remaining == 3  # AC-1.2: 3 darts available

def test_plain_dart_subtracts_face_value():
    game = Darts301()
    game.throw_dart(20)  # AC-2.1: Throw a dart with face value 20
    assert game.score == 281  # 301 - 20 = 281

def test_double_dart_subtracts_double_face_value():
    game = Darts301()
    game.throw_dart(20, double=True)  # AC-2.2: Throw a double dart with face value 20
    assert game.score == 261  # 301 - (20 * 2) = 261

def test_triple_dart_subtracts_triple_face_value():
    game = Darts301()
    game.throw_dart(20, triple=True)  # AC-2.3: Throw a triple dart with face value 20
    assert game.score == 241  # 301 - (20 * 3) = 241

def test_turn_ends_after_three_darts():
    game = Darts301()
    game.throw_dart(20)
    game.throw_dart(20)
    game.throw_dart(20)  # AC-3.1: Third dart ends the turn
    assert game.turn == 2  # Next turn number should be 2
    assert game.darts_remaining == 3  # Should have 3 darts available again

def test_bust_leaves_score_at_start_of_turn():
    game = Darts301()
    game.throw_dart(20)  # First throw
    game.throw_dart(20)  # Second throw
    game.throw_dart(1)  # AC-4.1: Third dart makes score 1 (301 - 20 - 20 - 1 = 260)
    assert game.score == 301  # Score should restore to 301
    assert game.darts_remaining == 3  # Turn ends, should have 3 darts available again
    assert not game.finished  # Game should not be finished

def test_bust_with_negative_score():
    game = Darts301()
    game.throw_dart(200)  # First throw
    game.throw_dart(150)  # Second throw
    game.throw_dart(1)  # AC-4.2: Third dart makes score negative (301 - 200 - 150 - 1 = -50)
    assert game.score == 301  # Score should restore to 301
    assert game.darts_remaining == 3  # Turn ends, should have 3 darts available again
    assert not game.finished  # Game should not be finished

def test_bust_with_zero_without_double():
    game = Darts301()
    game.throw_dart(20)  # First throw
    game.throw_dart(20)  # Second throw
    game.throw_dart(40)  # AC-4.3: Third dart makes score zero (301 - 20 - 20 - 40 = 221)
    assert game.score == 301  # Score should restore to 301
    assert game.darts_remaining == 3  # Turn ends, should have 3 darts available again
    assert not game.finished  # Game should not be finished

def test_winning_with_double():
    game = Darts301()
    game.throw_dart(20)  # First throw
    game.throw_dart(20)  # Second throw
    game.throw_dart(60, double=True)  # AC-5.1: Last dart is a double to make score 0
    assert game.score == 0  # Score should be 0
    assert game.finished  # Game should be finished

def test_darts_remaining_decreases_after_first_throw():
    game = Darts301()
    game.throw_dart(20)  # First throw
    assert game.darts_remaining == 2  # After first throw, 2 darts should remain

def test_darts_remaining_decreases_after_second_throw():
    game = Darts301()
    game.throw_dart(20)  # First throw
    game.throw_dart(20)  # Second throw
    assert game.darts_remaining == 1  # After second throw, 1 dart should remain

def test_bust_before_third_dart():
    game = Darts301()
    game.throw_dart(300)  # First throw
    game.throw_dart(10)  # AC-4.4: Second dart makes score negative (301 - 300 - 10 = -9)
    assert game.score == 301  # Score should restore to 301
    assert game.darts_remaining == 3  # Turn ends, should have 3 darts available again
    assert game.turn == 2  # Turn should advance to the next turn
    assert not game.finished  # Game should not be finished

def test_bust_on_third_dart():
    game = Darts301()
    game.throw_dart(20)  # First throw
    game.throw_dart(20)  # Second throw
    game.throw_dart(1)  # AC-4.1: Third dart leaves score 1, causing a bust
    assert game.score == 301  # Score should restore to 301
    assert game.darts_remaining == 3  # Turn ends, should have 3 darts available again
    assert game.turn == 2  # Turn should advance to the next turn
    assert not game.finished  # Game should not be finished