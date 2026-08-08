# test_darts.py

from solution import DartsGame

def test_new_game_starts_at_301():
    game = DartsGame()
    assert game.score == 301  # AC-1.1: A new game has a score of 301
    assert not game.is_finished  # AC-1.1: A new game is not finished
    assert game.turn_number == 1  # AC-1.2: A new game is on turn 1
    assert game.darts_remaining == 3  # AC-1.2: With 3 darts available

def test_plain_dart_subtracts_face_value():
    game = DartsGame()
    game.throw_dart(20)  # AC-2.1: Throw a plain dart with value 20
    assert game.score == 281  # 301 - 20 = 281

def test_double_dart_subtracts_double_face_value():
    game = DartsGame()
    game.throw_dart(20, double=True)  # AC-2.2: Throw a double dart with value 20
    assert game.score == 261  # 301 - (2 * 20) = 261

def test_triple_dart_subtracts_triple_face_value():
    game = DartsGame()
    game.throw_dart(20, triple=True)  # AC-2.3: Throw a triple dart with value 20
    assert game.score == 241  # 301 - (3 * 20) = 241

def test_turns_decrease_darts_remaining():
    game = DartsGame()
    game.throw_dart(20)
    assert game.darts_remaining == 2  # After one throw, 2 darts remaining
    game.throw_dart(15)
    assert game.darts_remaining == 1  # After two throws, 1 dart remaining
    game.throw_dart(10)
    assert game.darts_remaining == 3  # After the third throw, turn ends and resets darts

def test_turn_ends_after_three_throws():
    game = DartsGame()
    game.throw_dart(20)
    game.throw_dart(15)
    game.throw_dart(10)
    assert game.turn_number == 2  # After the turn ends, move to turn 2

def test_bust_when_score_is_one():
    game = DartsGame()
    game.throw_dart(300)  # First throw, score is now 1 (301 - 300 = 1)
    assert game.score == 301  # Score resets to start of turn
    assert game.darts_remaining == 3  # Turn ends immediately, all darts forfeited
    assert not game.is_finished  # Game remains unfinished

def test_bust_on_negative_score():
    game = DartsGame()
    game.throw_dart(250)  # First throw, score is now 51 (301 - 250 = 51)
    game.throw_dart(60)  # Second throw, score goes below zero (51 - 60 = -9)
    assert game.score == 301  # Score resets to start of turn
    assert game.darts_remaining == 3  # Turn ends immediately, all darts forfeited
    assert not game.is_finished  # Game remains unfinished

def test_bust_when_reaching_zero_without_double():
    game = DartsGame()
    game.throw_dart(150)  # First throw, score is now 151 (301 - 150 = 151)
    game.throw_dart(149)  # Second throw, score is now 2 (151 - 149 = 2)
    game.throw_dart(2)  # Third throw, score reaches zero without being a double
    assert game.score == 301  # Score resets to start of turn
    assert game.darts_remaining == 3  # Turn ends immediately, all darts forfeited
    assert not game.is_finished  # Game remains unfinished

def test_win_when_reaching_zero_with_double():
    game = DartsGame()
    game.throw_dart(150)  # First throw, score is now 151 (301 - 150 = 151)
    game.throw_dart(149)  # Second throw, score is now 2 (151 - 149 = 2)
    game.throw_dart(1, double=True)  # Third throw, score reaches zero with a double
    assert game.score == 0  # Score should be zero
    assert game.is_finished  # Game should be finished

def test_bust_on_third_dart_leaving_one():
    game = DartsGame()
    game.throw_dart(300)  # First throw, score is now 1 (301 - 300 = 1)
    game.throw_dart(149)  # Second throw, score is now 2 (1 - 149 = -147)
    assert game.score == 301  # Score resets to start of turn
    assert game.darts_remaining == 3  # Turn ends immediately, all darts forfeited
    assert not game.is_finished  # Game remains unfinished

def test_bust_after_completed_turn():
    game = DartsGame()
    game.throw_dart(20)  # First throw
    game.throw_dart(15)  # Second throw
    game.throw_dart(10)  # Third throw, turn ends
    assert game.turn_number == 2  # Move to turn 2
    game.throw_dart(150)  # First throw, score is now 151 (301 - 150 = 151)
    game.throw_dart(149)  # Second throw, score is now 2 (151 - 149 = 2)
    game.throw_dart(2)  # Third throw, score reaches zero without being a double
    assert game.score == 301  # Score resets to start of turn
    assert game.darts_remaining == 3  # Turn ends immediately, all darts forfeited
    assert not game.is_finished  # Game remains unfinished