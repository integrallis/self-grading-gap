# test_tennis_game.py

from solution import TennisGame

def test_initial_score():
    game = TennisGame()
    # Both players start at "0"
    assert game.score() == ("0", "0")

def test_player1_wins_first_point():
    game = TennisGame()
    game.player1_scores()
    # Player 1 scores, so the score is now "15" for player 1, "0" for player 2
    assert game.score() == ("15", "0")

def test_player2_wins_first_point():
    game = TennisGame()
    game.player2_scores()
    # Player 2 scores, so the score is now "0" for player 1, "15" for player 2
    assert game.score() == ("0", "15")

def test_player1_wins_second_point():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()  # Player 1 scores again
    # Player 1 has "30", Player 2 has "0"
    assert game.score() == ("30", "0")

def test_player1_wins_third_point():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()  # Player 1 scores again
    # Player 1 has "40", Player 2 has "0"
    assert game.score() == ("40", "0")

def test_player1_wins_game():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()  # Player 1 scores again to win the game
    # Player 1 wins the game
    assert game.winner() == "Player 1"

def test_no_winner_when_both_players_under_4_points():
    game = TennisGame()
    game.player1_scores()
    game.player2_scores()
    # No player has won yet, less than 4 points for both
    assert game.winner() is None

def test_deuce_and_advantage():
    game = TennisGame()
    # Both players score to reach 40
    for _ in range(3):
        game.player1_scores()
        game.player2_scores()
    assert game.score() == ("40", "40")

    game.player1_scores()  # Player 1 has advantage
    assert game.score() == ("A", "40")
    assert game.winner() is None

    game.player2_scores()  # Back to deuce
    assert game.score() == ("40", "40")
    assert game.winner() is None

    game.player2_scores()  # Player 2 has advantage
    assert game.score() == ("40", "A")
    assert game.winner() is None

    game.player1_scores()  # Back to deuce again
    assert game.score() == ("40", "40")
    assert game.winner() is None

    game.player2_scores()  # Player 2 has advantage again
    assert game.score() == ("40", "A")
    assert game.winner() is None

    game.player2_scores()  # Player 2 wins the game
    assert game.winner() == "Player 2"

def test_player_with_advantage_wins_game():
    game = TennisGame()
    # Both players score to reach 40
    for _ in range(3):
        game.player1_scores()
        game.player2_scores()
    assert game.score() == ("40", "40")

    game.player1_scores()  # Player 1 has advantage
    assert game.score() == ("A", "40")
    assert game.winner() is None

    game.player1_scores()  # Player 1 wins the game
    assert game.winner() == "Player 1"