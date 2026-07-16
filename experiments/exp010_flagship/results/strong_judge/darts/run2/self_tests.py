from solution import DartsGame

def test_new_game_initial_conditions():
    game = DartsGame()
    assert game.score == 301  # AC-1.1: New game starts at 301
    assert game.turn == 1  # AC-1.2: New game starts at turn 1
    assert game.darts_remaining == 3  # AC-1.2: New game starts with 3 darts available
    assert not game.finished  # AC-1.1: Game is not finished

def test_plain_dart_scoring():
    game = DartsGame()
    game.throw_dart(20)  # AC-2.1: Throw a plain dart with value 20
    assert game.score == 281  # 301 - 20 = 281

def test_double_dart_scoring():
    game = DartsGame()
    game.throw_dart(10, is_double=True)  # AC-2.2: Throw a double dart with value 10
    assert game.score == 281  # 301 - (10 * 2) = 281

def test_triple_dart_scoring():
    game = DartsGame()
    game.throw_dart(5, is_triple=True)  # AC-2.3: Throw a triple dart with value 5
    assert game.score == 286  # 301 - (5 * 3) = 286

def test_turns_of_three_darts():
    game = DartsGame()
    game.throw_dart(20)
    assert game.darts_remaining == 2  # 2 darts remaining after 1 throw
    game.throw_dart(15)
    assert game.darts_remaining == 1  # 1 dart remaining after 2 throws
    game.throw_dart(10)
    assert game.darts_remaining == 3  # 3 darts available for the next turn
    assert game.turn == 2  # Next turn is 2

def test_bust_exactly_one():
    game = DartsGame()
    game.throw_dart(20)  # First throw to 281
    game.throw_dart(10)  # Second throw to 271
    game.throw_dart(20)  # AC-4.1: Final throw leaves exactly 1
    assert game.score == 301  # Bust restores score to the start of the turn
    assert game.darts_remaining == 3  # Turn ends immediately, 3 darts available again
    assert not game.finished  # Game is unfinished after bust

def test_bust_below_zero():
    game = DartsGame()
    game.throw_dart(20)  # First throw to 281
    game.throw_dart(10)  # Second throw to 271
    game.throw_dart(300)  # AC-4.2: Final throw takes score below zero
    assert game.score == 301  # Bust restores score to the start of the turn
    assert game.darts_remaining == 3  # Turn ends immediately, 3 darts available again
    assert not game.finished  # Game is unfinished after bust

def test_bust_without_double():
    game = DartsGame()
    game.throw_dart(20)  # First throw to 281
    game.throw_dart(10)  # Second throw to 271
    game.throw_dart(271)  # AC-4.3: Final throw reaches exactly zero without being a double
    assert game.score == 301  # Bust restores score to the start of the turn
    assert game.darts_remaining == 3  # Turn ends immediately, 3 darts available again
    assert not game.finished  # Game is unfinished after bust

def test_bust_on_first_dart():
    game = DartsGame()
    game.throw_dart(20)  # First throw to 281
    game.throw_dart(10)  # Second throw to 271
    game.throw_dart(270)  # AC-4.2: Final throw takes score below zero
    assert game.score == 301  # Bust restores score to the start of the turn
    assert game.darts_remaining == 3  # Turn ends immediately, 3 darts available again
    assert not game.finished  # Game is unfinished after bust

def test_winning_with_double():
    game = DartsGame()
    game.throw_dart(1)  # First throw to 300
    game.throw_dart(1, is_double=True)  # AC-5.1: Final throw with double to reach exactly zero
    assert game.finished  # Game is finished