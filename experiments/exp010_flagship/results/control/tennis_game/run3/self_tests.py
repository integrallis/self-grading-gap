# test_tennis_scoring.py

from solution import TennisGame

def test_initial_score_is_zero():
    game = TennisGame()
    assert game.score() == ("0", "0")  # AC-2.1: Both players start at "0"

def test_player1_scores_first_point():
    game = TennisGame()
    game.player1_scores()
    assert game.score() == ("15", "0")  # AC-2.2: Player 1 scores, Player 2 remains at "0"

def test_player2_scores_first_point():
    game = TennisGame()
    game.player2_scores()
    assert game.score() == ("0", "15")  # AC-2.2: Player 2 scores, Player 1 remains at "0"

def test_player1_scores_to_30():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()  # Player 1 scores twice
    assert game.score() == ("30", "0")  # AC-2.2: Player 1 at "30", Player 2 at "0"

def test_player2_scores_to_30():
    game = TennisGame()
    game.player2_scores()
    game.player2_scores()  # Player 2 scores twice
    assert game.score() == ("0", "30")  # AC-2.2: Player 2 at "30", Player 1 at "0"

def test_player1_scores_to_40():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()  # Player 1 scores three times
    assert game.score() == ("40", "0")  # AC-2.2: Player 1 at "40", Player 2 at "0"

def test_player2_scores_to_40():
    game = TennisGame()
    game.player2_scores()
    game.player2_scores()
    game.player2_scores()  # Player 2 scores three times
    assert game.score() == ("0", "40")  # AC-2.2: Player 2 at "40", Player 1 at "0"

def test_no_winner_below_4_points():
    game = TennisGame()
    game.player1_scores()
    game.player2_scores()
    assert game.winner() is None  # AC-3.1: No winner while neither has 4 points

def test_player1_wins_game_from_40():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()  # Player 1 to "40"
    game.player2_scores()  # Player 2 to "40"
    game.player1_scores()  # Player 1 wins
    assert game.winner() == 1  # AC-3.2: Player 1 wins

def test_player2_wins_game_from_40():
    game = TennisGame()
    game.player2_scores()
    game.player2_scores()
    game.player2_scores()  # Player 2 to "40"
    game.player1_scores()  # Player 1 to "40"
    game.player2_scores()  # Player 2 wins
    assert game.winner() == 2  # AC-3.2: Player 2 wins

def test_deuce_to_advantage_player1():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()  # Player 1 to "40"
    game.player2_scores()  # Player 2 to "40"
    game.player1_scores()  # Player 1 gets advantage
    assert game.score() == ("A", "40")  # AC-4.1: Player 1 has advantage

def test_deuce_to_advantage_player2():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()  # Player 1 to "40"
    game.player2_scores()  # Player 2 to "40"
    game.player2_scores()  # Player 2 gets advantage
    assert game.score() == ("40", "A")  # AC-4.1: Player 2 has advantage

def test_advantage_player1_wins_game():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()  # Player 1 to "40"
    game.player2_scores()  # Player 2 to "40"
    game.player1_scores()  # Player 1 gets advantage
    game.player1_scores()  # Player 1 wins
    assert game.winner() == 1  # AC-4.3: Player 1 wins

def test_advantage_player2_wins_game():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()  # Player 1 to "40"
    game.player2_scores()  # Player 2 to "40"
    game.player2_scores()  # Player 2 gets advantage
    game.player2_scores()  # Player 2 wins
    assert game.winner() == 2  # AC-4.3: Player 2 wins

def test_return_to_deuce_from_advantage():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()  # Player 1 to "40"
    game.player2_scores()  # Player 2 to "40"
    game.player1_scores()  # Player 1 has advantage
    game.player2_scores()  # Player 2 returns to deuce
    assert game.score() == ("40", "40")  # AC-4.2: Return to deuce