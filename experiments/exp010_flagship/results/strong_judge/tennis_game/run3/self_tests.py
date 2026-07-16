from solution import TennisGame

def test_initial_scores_are_zero():
    game = TennisGame()
    assert game.score() == ("0", "0")  # both players start at 0

def test_player_one_scores_first_point():
    game = TennisGame()
    game.player_one_scores()
    assert game.score() == ("15", "0")  # player one moves to 15

def test_player_two_scores_first_point():
    game = TennisGame()
    game.player_two_scores()
    assert game.score() == ("0", "15")  # player two moves to 15

def test_player_one_scores_two_points():
    game = TennisGame()
    game.player_one_scores()
    game.player_one_scores()
    assert game.score() == ("30", "0")  # player one moves to 30

def test_player_two_scores_two_points():
    game = TennisGame()
    game.player_two_scores()
    game.player_two_scores()
    assert game.score() == ("0", "30")  # player two moves to 30

def test_player_one_scores_three_points():
    game = TennisGame()
    game.player_one_scores()
    game.player_one_scores()
    game.player_one_scores()
    assert game.score() == ("40", "0")  # player one moves to 40

def test_player_two_scores_three_points():
    game = TennisGame()
    game.player_two_scores()
    game.player_two_scores()
    game.player_two_scores()
    assert game.score() == ("0", "40")  # player two moves to 40

def test_player_one_wins_game_from_40():
    game = TennisGame()
    game.player_one_scores()
    game.player_one_scores()
    game.player_one_scores()  # player one is at 40
    game.player_one_scores()  # player one should win
    assert game.winner() == 1  # player one wins

def test_player_two_wins_game_from_40():
    game = TennisGame()
    game.player_two_scores()
    game.player_two_scores()
    game.player_two_scores()  # player two is at 40
    game.player_two_scores()  # player two should win
    assert game.winner() == 2  # player two wins

def test_no_winner_below_four_points():
    game = TennisGame()
    game.player_one_scores()  # player one at 15
    game.player_two_scores()  # player two at 15
    assert game.winner() is None  # no winner yet

def test_deuce_and_advantage():
    game = TennisGame()
    game.player_one_scores()  # 15
    game.player_two_scores()  # 15
    game.player_one_scores()  # 30
    game.player_two_scores()  # 30
    game.player_one_scores()  # 40
    game.player_two_scores()  # 40
    game.player_one_scores()  # player one to advantage
    assert game.score() == ("A", "40")  # player one has advantage
    assert game.winner() is None  # no winner yet

def test_return_to_deuce():
    game = TennisGame()
    game.player_one_scores()  # 15
    game.player_two_scores()  # 15
    game.player_one_scores()  # 30
    game.player_two_scores()  # 30
    game.player_one_scores()  # 40
    game.player_two_scores()  # 40
    game.player_one_scores()  # player one to advantage
    game.player_two_scores()  # player two returns to deuce
    assert game.score() == ("40", "40")  # back to deuce
    assert game.winner() is None  # no winner yet

def test_player_one_wins_game_from_advantage():
    game = TennisGame()
    game.player_one_scores()  # 15
    game.player_two_scores()  # 15
    game.player_one_scores()  # 30
    game.player_two_scores()  # 30
    game.player_one_scores()  # 40
    game.player_two_scores()  # 40
    game.player_one_scores()  # player one to advantage
    game.player_one_scores()  # player one wins
    assert game.winner() == 1  # player one wins

def test_player_two_wins_game_from_advantage():
    game = TennisGame()
    game.player_one_scores()  # 15
    game.player_two_scores()  # 15
    game.player_one_scores()  # 30
    game.player_two_scores()  # 30
    game.player_one_scores()  # 40
    game.player_two_scores()  # 40
    game.player_two_scores()  # player two to advantage
    game.player_two_scores()  # player two wins
    assert game.winner() == 2  # player two wins

def test_return_to_deuce_from_player_two_advantage():
    game = TennisGame()
    game.player_one_scores()  # 15
    game.player_two_scores()  # 15
    game.player_one_scores()  # 30
    game.player_two_scores()  # 30
    game.player_one_scores()  # 40
    game.player_two_scores()  # 40
    game.player_two_scores()  # player two to advantage
    game.player_one_scores()  # back to deuce
    assert game.score() == ("40", "40")  # back to deuce

def test_repeated_deuce_cycle():
    game = TennisGame()
    game.player_one_scores()  # 15
    game.player_two_scores()  # 15
    game.player_one_scores()  # 30
    game.player_two_scores()  # 30
    game.player_one_scores()  # 40
    game.player_two_scores()  # 40
    game.player_one_scores()  # player one to advantage
    game.player_two_scores()  # back to deuce
    assert game.score() == ("40", "40")  # back to deuce
    game.player_two_scores()  # player two to advantage
    assert game.score() == ("40", "A")  # player two has advantage
    game.player_one_scores()  # back to deuce again
    assert game.score() == ("40", "40")  # back to deuce again