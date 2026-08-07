from solution import DartsGame

def test_new_game_starts_at_301():
    game = DartsGame()
    assert game.score == 301  # AC-1.1: A new game has a score of 301
    assert not game.finished  # AC-1.1: Game is not finished
    assert game.turn == 1  # AC-1.2: A new game is on turn 1
    assert game.darts_remaining == 3  # AC-1.2: 3 darts available

def test_plain_dart_subtracts_face_value():
    game = DartsGame()
    game.throw_dart(20)  # AC-2.1: Throw a dart worth 20
    assert game.score == 281  # 301 - 20 = 281

def test_double_dart_subtracts_double_face_value():
    game = DartsGame()
    game.throw_dart(20, double=True)  # AC-2.2: Throw a double dart worth 20
    assert game.score == 261  # 301 - (2 * 20) = 261

def test_triple_dart_subtracts_triple_face_value():
    game = DartsGame()
    game.throw_dart(20, triple=True)  # AC-2.3: Throw a triple dart worth 20
    assert game.score == 241  # 301 - (3 * 20) = 241

def test_turn_decreases_darts_remaining():
    game = DartsGame()
    game.throw_dart(20)
    assert game.darts_remaining == 2  # After one dart, 2 remaining
    game.throw_dart(20)
    assert game.darts_remaining == 1  # After two darts, 1 remaining
    game.throw_dart(20)  # Third dart, end turn
    assert game.turn == 2  # AC-3.1: Next turn number
    assert game.darts_remaining == 3  # AC-3.1: 3 darts available again

def test_bust_when_last_dart_leaves_score_one():
    game = DartsGame()
    game.throw_dart(300)  # 301 - 300 = 1
    game.throw_dart(1)  # This throw results in a bust
    assert game.score == 301  # AC-4.4: Score restored to 301
    assert game.turn == 2  # AC-4.4: Turn number advanced
    assert game.darts_remaining == 3  # AC-4.4: Darts remaining reset
    assert not game.finished  # AC-4.4: Game is not finished

def test_bust_when_score_below_zero():
    game = DartsGame()
    game.throw_dart(100)  # 301 - 100 = 201
    game.throw_dart(202)  # This throw results in a bust
    assert game.score == 301  # AC-4.2: Score restored to 301
    assert game.turn == 2  # AC-4.4: Turn number advanced
    assert game.darts_remaining == 3  # AC-4.4: Darts remaining reset
    assert not game.finished  # AC-4.4: Game is not finished

def test_bust_when_reaching_zero_without_double():
    game = DartsGame()
    game.throw_dart(301)  # 301 - 301 = 0 (not a double)
    assert game.score == 301  # AC-4.3: Score restored to 301
    assert game.turn == 2  # AC-4.4: Turn number advanced
    assert game.darts_remaining == 3  # AC-4.4: Darts remaining reset
    assert not game.finished  # AC-4.4: Game is not finished

def test_winning_with_double():
    game = DartsGame()
    game.throw_dart(100)  # 301 - 100 = 201
    game.throw_dart(101)  # 201 - 101 = 100
    game.throw_dart(50, double=True)  # 100 - (2 * 50) = 0, winning move
    assert game.finished  # AC-5.1: Game is finished
    assert game.score == 0  # AC-5.1: Score is zero