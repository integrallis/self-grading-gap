# test_tennis.py

from solution import TennisGame

def test_initial_scores():
    game = TennisGame()
    assert game.score() == ("0", "0")  # AC-2.1: New game starts with both players announced at "0"

def test_player_one_wins_first_point():
    game = TennisGame()
    game.player_one_scores()
    assert game.score() == ("15", "0")  # AC-2.2: Player one wins a point, score advances to "15"

def test_player_two_wins_first_point():
    game = TennisGame()
    game.player_two_scores()
    assert game.score() == ("0", "15")  # AC-2.2: Player two wins a point, score advances to "15"

def test_player_one_wins_second_point():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    assert game.score() == ("30", "0")  # Player one has 30, player two still at 0

def test_player_one_wins_third_point():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    assert game.score() == ("40", "0")  # Player one has 40, player two still at 0

def test_player_one_wins_game():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    game.player_one_scores()  # 40 -> WIN
    assert game.winner() is None  # AC-3.1: No winner while neither player has scored more than three points
    game.player_one_scores()  # 40 -> WIN
    assert game.winner() == "Player 1"  # AC-3.2: Player one wins the game

def test_player_two_wins_game():
    game = TennisGame()
    game.player_two_scores()  # 0 -> 15
    game.player_two_scores()  # 15 -> 30
    game.player_two_scores()  # 30 -> 40
    game.player_two_scores()  # 40 -> WIN
    assert game.winner() is None  # AC-3.1: No winner while neither player has scored more than three points
    game.player_two_scores()  # 40 -> WIN
    assert game.winner() == "Player 2"  # AC-3.2: Player two wins the game

def test_no_winner_before_four_points():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_two_scores()  # 0 -> 15
    assert game.winner() is None  # AC-3.1: No winner while neither player has scored more than three points

def test_deuce_situation():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_two_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_two_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    game.player_two_scores()  # 30 -> 40
    assert game.score() == ("40", "40")  # Both players at 40 (deuce)

def test_advantage_player_one():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_two_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_two_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    game.player_two_scores()  # 30 -> 40
    game.player_one_scores()  # 40 -> A
    assert game.score() == ("A", "40")  # Player one has advantage
    assert game.winner() is None  # Game still has no winner

def test_advantage_lost():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_two_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_two_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    game.player_two_scores()  # 30 -> 40
    game.player_one_scores()  # 40 -> A
    game.player_two_scores()  # A -> deuce
    assert game.score() == ("40", "40")  # Both players back to deuce

def test_player_one_wins_with_advantage():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_two_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_two_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    game.player_two_scores()  # 30 -> 40
    game.player_one_scores()  # 40 -> A
    game.player_one_scores()  # A -> WIN
    assert game.winner() == "Player 1"  # AC-4.3: Player one wins with advantage

def test_player_two_wins_with_advantage():
    game = TennisGame()
    game.player_two_scores()  # 0 -> 15
    game.player_one_scores()  # 0 -> 15
    game.player_two_scores()  # 15 -> 30
    game.player_one_scores()  # 15 -> 30
    game.player_two_scores()  # 30 -> 40
    game.player_one_scores()  # 30 -> 40
    game.player_two_scores()  # 40 -> A
    game.player_two_scores()  # A -> WIN
    assert game.winner() == "Player 2"  # AC-4.3: Player two wins with advantage

def test_multiple_deuce_advantage_cycles():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_two_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_two_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    game.player_two_scores()  # 30 -> 40
    game.player_one_scores()  # 40 -> A
    game.player_two_scores()  # A -> 40
    game.player_two_scores()  # 40 -> A
    game.player_one_scores()  # A -> 40
    game.player_two_scores()  # 40 -> A
    game.player_two_scores()  # A -> WIN
    assert game.winner() == "Player 2"  # Player two wins after multiple cycles

def test_no_advantage_for_player_with_0():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    game.player_two_scores()  # 0 -> 15
    assert game.score() == ("40", "15")  # AC-4.4: Player one is announced as "40", player two as "15"