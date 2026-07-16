from solution import Game

def test_new_game_start():
    game = Game()
    assert game.score == 301  # AC-1.1: New game starts at 301
    assert not game.finished  # AC-1.1: Game is not finished
    assert game.turn == 1  # AC-1.2: Game is on turn 1
    assert game.darts_remaining == 3  # AC-1.2: 3 darts available

def test_plain_dart_score():
    game = Game()
    game.throw_dart(20)  # AC-2.1: Throw a plain dart worth 20
    assert game.score == 281  # 301 - 20 = 281

def test_double_dart_score():
    game = Game()
    game.throw_dart(20, double=True)  # AC-2.2: Throw a double dart worth 20
    assert game.score == 261  # 301 - (2 * 20) = 261

def test_triple_dart_score():
    game = Game()
    game.throw_dart(20, triple=True)  # AC-2.3: Throw a triple dart worth 20
    assert game.score == 241  # 301 - (3 * 20) = 241

def test_turns_of_three_darts():
    game = Game()
    game.throw_dart(20)
    assert game.darts_remaining == 2  # AC-3.1: 2 darts remaining after one throw
    game.throw_dart(20)
    assert game.darts_remaining == 1  # AC-3.1: 1 dart remaining after second throw
    game.throw_dart(20)  # Third throw
    assert game.darts_remaining == 3  # AC-3.1: Turn ends, darts reset to 3
    assert game.turn == 2  # AC-3.1: Next turn is 2

def test_bust_from_one():
    game = Game()
    game.throw_dart(2)
    game.throw_dart(1)  # AC-4.1: Throw leaves score at 1
    assert game.score == 2  # AC-4.4: Bust restores score to start of turn
    assert game.darts_remaining == 3  # AC-4.4: Turn ends immediately
    assert game.turn == 2  # AC-4.4: Next turn number is incremented
    assert not game.finished  # AC-4.4: Game is not finished

def test_bust_below_zero():
    game = Game()
    game.throw_dart(20)
    game.throw_dart(19)  # AC-4.2: Throw takes score to 1
    game.throw_dart(2)  # Throws a value greater than remaining score
    assert game.score == 1  # AC-4.4: Bust restores score to start of turn
    assert game.darts_remaining == 3  # AC-4.4: Turn ends immediately
    assert game.turn == 2  # AC-4.4: Next turn number is incremented
    assert not game.finished  # AC-4.4: Game is not finished

def test_bust_not_double():
    game = Game()
    game.throw_dart(20)
    game.throw_dart(1)  # AC-4.3: Throws leave score at 20
    game.throw_dart(20)  # Final throw that takes score to 0 but not a double
    assert game.score == 20  # AC-4.4: Bust restores score to start of turn
    assert game.darts_remaining == 3  # AC-4.4: Turn ends immediately
    assert game.turn == 2  # AC-4.4: Next turn number is incremented
    assert not game.finished  # AC-4.4: Game is not finished

def test_win_with_double():
    game = Game()
    game.throw_dart(20)
    game.throw_dart(20)
    game.throw_dart(10, double=True)  # AC-5.1: Winning throw with a double
    assert game.score == 0  # Game ends with score at 0
    assert game.finished  # Game is finished

def test_bust_on_final_dart():
    game = Game()
    game.throw_dart(2)
    game.throw_dart(1)  # Throw leaves score at 1
    game.throw_dart(1)  # Final throw that leaves score at 0 but not a double
    assert game.score == 1  # AC-4.4: Bust restores score to start of turn
    assert game.darts_remaining == 3  # AC-4.4: Turn ends immediately
    assert game.turn == 2  # AC-4.4: Next turn number is incremented
    assert not game.finished  # AC-4.4: Game is not finished