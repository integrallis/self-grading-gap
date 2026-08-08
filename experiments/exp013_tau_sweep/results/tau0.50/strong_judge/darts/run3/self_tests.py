from solution import DartsGame

def test_new_game_starts_at_301():
    game = DartsGame()
    assert game.score == 301  # AC-1.1: A new game has a score of 301
    assert not game.is_finished  # AC-1.1: The game is not finished
    assert game.turn_number == 1  # AC-1.2: The game is on turn 1
    assert game.darts_remaining == 3  # AC-1.2: 3 darts available

def test_plain_dart_score_subtraction():
    game = DartsGame()
    game.throw_dart(20)  # AC-2.1: Throw a dart with face value 20
    assert game.score == 281  # 301 - 20 = 281

def test_double_dart_score_subtraction():
    game = DartsGame()
    game.throw_dart(20, is_double=True)  # AC-2.2: Throw a double dart with face value 20
    assert game.score == 261  # 301 - (2 * 20) = 261

def test_triple_dart_score_subtraction():
    game = DartsGame()
    game.throw_dart(20, is_triple=True)  # AC-2.3: Throw a triple dart with face value 20
    assert game.score == 241  # 301 - (3 * 20) = 241

def test_turns_of_three_darts():
    game = DartsGame()
    game.throw_dart(20)
    assert game.darts_remaining == 2  # After first throw, 2 darts remaining
    game.throw_dart(15)
    assert game.darts_remaining == 1  # After second throw, 1 dart remaining
    game.throw_dart(10)  # AC-3.1: Three darts thrown
    assert game.turn_number == 2  # Next turn number after three darts
    assert game.darts_remaining == 3  # New turn has 3 darts available

def test_bust_leaving_one():
    game = DartsGame()
    game.throw_dart(20)  # Score: 281
    game.throw_dart(20)  # Score: 261
    game.throw_dart(20)  # Score: 241
    game.throw_dart(20)  # Score: 221
    game.throw_dart(20)  # Score: 201
    game.throw_dart(20)  # Score: 181
    game.throw_dart(20)  # Score: 161
    game.throw_dart(20)  # Score: 141
    game.throw_dart(20)  # Score: 121
    game.throw_dart(20)  # Score: 101
    game.throw_dart(20)  # Score: 81
    game.throw_dart(20)  # Score: 61
    game.throw_dart(20)  # Score: 41
    game.throw_dart(20)  # Score: 21
    game.throw_dart(20)  # Score: 1; this is a bust
    assert game.score == 61  # Score should reset to starting value
    assert game.darts_remaining == 3  # Turn ends, 3 darts available
    assert not game.is_finished  # Game is still unfinished

def test_bust_below_zero():
    game = DartsGame()
    game.throw_dart(20)  # Score: 281
    game.throw_dart(20)  # Score: 241
    game.throw_dart(20)  # Score: 201
    game.throw_dart(20)  # Score: 181
    game.throw_dart(20)  # Score: 161
    game.throw_dart(20)  # Score: 141
    game.throw_dart(20)  # Score: 121
    game.throw_dart(20)  # Score: 101
    game.throw_dart(20)  # Score: 81
    game.throw_dart(20)  # Score: 61
    game.throw_dart(20)  # Score: 41
    game.throw_dart(20)  # Score: 21
    game.throw_dart(20)  # Score: 1
    game.throw_dart(20, is_triple=True)  # Score: -19; this is a bust
    assert game.score == 61  # Score should reset to starting value
    assert game.darts_remaining == 3  # Turn ends, 3 darts available
    assert not game.is_finished  # Game is still unfinished

def test_bust_reaching_zero_without_double():
    game = DartsGame()
    game.throw_dart(20)  # Score: 281
    game.throw_dart(20)  # Score: 261
    game.throw_dart(20)  # Score: 241
    game.throw_dart(20)  # Score: 221
    game.throw_dart(20)  # Score: 201
    game.throw_dart(20)  # Score: 181
    game.throw_dart(20)  # Score: 161
    game.throw_dart(20)  # Score: 141
    game.throw_dart(20)  # Score: 121
    game.throw_dart(20)  # Score: 101
    game.throw_dart(20)  # Score: 81
    game.throw_dart(20)  # Score: 61
    game.throw_dart(20)  # Score: 41
    game.throw_dart(20)  # Score: 21
    game.throw_dart(20)  # Score: 1
    game.throw_dart(21)  # Score: 0; this is a bust
    assert game.score == 61  # Score should reset to 61
    assert game.darts_remaining == 3  # Turn ends, 3 darts available
    assert not game.is_finished  # Game is still unfinished

def test_winning_with_double():
    game = DartsGame()
    game.throw_dart(20)  # Score: 281
    game.throw_dart(20)  # Score: 261
    game.throw_dart(20)  # Score: 241
    game.throw_dart(20)  # Score: 221
    game.throw_dart(20)  # Score: 201
    game.throw_dart(20)  # Score: 181
    game.throw_dart(20)  # Score: 161
    game.throw_dart(20)  # Score: 141
    game.throw_dart(20)  # Score: 121
    game.throw_dart(20)  # Score: 101
    game.throw_dart(20)  # Score: 81
    game.throw_dart(20)  # Score: 61
    game.throw_dart(20)  # Score: 41
    game.throw_dart(20)  # Score: 21
    game.throw_dart(20)  # Score: 1
    game.throw_dart(20, is_double=True)  # Score: 0; this is a winning double
    assert game.score == 0  # Score should be zero
    assert game.is_finished  # Game is finished