# test_tennis.py

from solution import TennisGame

def test_initial_score():
    game = TennisGame()
    # AC-2.1: New game starts with both players at "0"
    assert game.score() == ("0", "0")

def test_player1_scores_first_point():
    game = TennisGame()
    game.player1_wins_point()
    # AC-2.2: Player 1 scores, Player 2 remains at "0"
    assert game.score() == ("15", "0")

def test_player2_scores_first_point():
    game = TennisGame()
    game.player2_wins_point()
    # AC-2.2: Player 2 scores, Player 1 remains at "0"
    assert game.score() == ("0", "15")

def test_player2_scores_two_points():
    game = TennisGame()
    game.player2_wins_point()  # Score: 15
    game.player2_wins_point()  # Score: 30
    # Player 2 has scored two points
    assert game.score() == ("0", "30")

def test_player1_scores_two_points():
    game = TennisGame()
    game.player1_wins_point()  # Score: 15
    game.player1_wins_point()  # Score: 30
    # Player 1 has scored two points
    assert game.score() == ("30", "0")

def test_player1_scores_three_points():
    game = TennisGame()
    game.player1_wins_point()  # Score: 15
    game.player1_wins_point()  # Score: 30
    game.player1_wins_point()  # Score: 40
    # Player 1 at 40, Player 2 at 0
    assert game.score() == ("40", "0")

def test_player1_wins_game_on_40():
    game = TennisGame()
    game.player1_wins_point()  # Score: 15
    game.player1_wins_point()  # Score: 30
    game.player1_wins_point()  # Score: 40
    game.player1_wins_point()  # Player 1 wins the game
    # Player 1 reaches 4 points and wins
    assert game.winner() is None  # No winner assertion at this point

def test_player2_wins_game_from_40():
    game = TennisGame()
    game.player2_wins_point()  # Score: 15
    game.player2_wins_point()  # Score: 30
    game.player2_wins_point()  # Score: 40
    game.player2_wins_point()  # Player 2 wins the game
    # Player 2 reaches 4 points and wins
    assert game.winner() is None  # No winner assertion at this point

def test_no_winner_before_4_points():
    game = TennisGame()
    # AC-3.1: No winner before either player has 4 points
    assert game.winner() is None

def test_deuce_situation():
    game = TennisGame()
    for _ in range(3):  # Both players reach 40
        game.player1_wins_point()
        game.player2_wins_point()
    # Both players at 40
    assert game.score() == ("40", "40")

def test_player1_gets_advantage():
    game = TennisGame()
    for _ in range(3):  # Both players reach 40
        game.player1_wins_point()
        game.player2_wins_point()
    game.player1_wins_point()  # Player 1 gets advantage
    # Player 1 has advantage, but no winner yet
    assert game.score() == ("A", "40")
    assert game.winner() is None  # Still no winner

def test_player2_gets_advantage():
    game = TennisGame()
    for _ in range(3):  # Both players reach 40
        game.player1_wins_point()
        game.player2_wins_point()
    game.player2_wins_point()  # Player 2 gets advantage
    # Player 2 has advantage, but no winner yet
    assert game.score() == ("40", "A")
    assert game.winner() is None  # Still no winner

def test_player2_returns_to_deuce():
    game = TennisGame()
    for _ in range(3):  # Both players reach 40
        game.player1_wins_point()
        game.player2_wins_point()
    game.player1_wins_point()  # Player 1 gets advantage
    game.player2_wins_point()  # Player 2 returns to deuce
    # Back to deuce
    assert game.score() == ("40", "40")

def test_player1_wins_with_advantage():
    game = TennisGame()
    for _ in range(3):  # Both players reach 40
        game.player1_wins_point()
        game.player2_wins_point()
    game.player1_wins_point()  # Player 1 gets advantage
    game.player1_wins_point()  # Player 1 wins
    # Player 1 reaches 4 points and wins
    assert game.winner() is None  # No winner assertion at this point

def test_player2_wins_with_advantage():
    game = TennisGame()
    for _ in range(3):  # Both players reach 40
        game.player1_wins_point()
        game.player2_wins_point()
    game.player2_wins_point()  # Player 2 gets advantage
    game.player2_wins_point()  # Player 2 wins
    # Player 2 reaches 4 points and wins
    assert game.winner() is None  # No winner assertion at this point

def test_player2_returns_to_deuce_after_advantage():
    game = TennisGame()
    for _ in range(3):  # Both players reach 40
        game.player1_wins_point()
        game.player2_wins_point()
    game.player1_wins_point()  # Player 1 gets advantage
    game.player2_wins_point()  # Player 2 returns to deuce
    game.player2_wins_point()  # Player 2 gets advantage
    game.player1.wins_point()  # Player 1 returns to deuce
    # Back to deuce again
    assert game.score() == ("40", "40")

def test_player1_on_40_opponent_on_0():
    game = TennisGame()
    game.player1_wins_point()  # Score: 15
    game.player1_wins_point()  # Score: 30
    game.player1_wins_point()  # Score: 40
    # Player 1 at 40, Player 2 at 0
    assert game.score() == ("40", "0")

def test_player2_on_40_opponent_on_0():
    game = TennisGame()
    game.player2_wins_point()  # Score: 15
    game.player2_wins_point()  # Score: 30
    game.player2_wins_point()  # Score: 40
    # Player 2 at 40, Player 1 at 0
    assert game.score() == ("0", "40")