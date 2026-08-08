# test_tennis_game.py

from solution import TennisGame

def test_initial_scores_are_zero():
    game = TennisGame()
    assert game.score() == ("0", "0")  # Both players start at "0"

def test_first_point_player_1():
    game = TennisGame()
    game.player1_wins_point()
    assert game.score() == ("15", "0")  # Player 1 wins point, Player 2 remains at "0"

def test_first_point_player_2():
    game = TennisGame()
    game.player2_wins_point()
    assert game.score() == ("0", "15")  # Player 2 wins point, Player 1 remains at "0"

def test_second_point_player_1():
    game = TennisGame()
    game.player1_wins_point()
    game.player1_wins_point()
    assert game.score() == ("30", "0")  # Player 1 has two points, Player 2 remains at "0"

def test_third_point_player_1():
    game = TennisGame()
    game.player1_wins_point()
    game.player1_wins_point()
    game.player1_wins_point()
    assert game.score() == ("40", "0")  # Player 1 is at "40", Player 2 at "0"

def test_winning_game_player_1():
    game = TennisGame()
    game.player1_wins_point()
    game.player1_wins_point()
    game.player1_wins_point()
    game.player1_wins_point()
    assert game.winner() == "Player 1"  # Player 1 wins after scoring beyond "40"

def test_winning_game_player_2():
    game = TennisGame()
    game.player2_wins_point()
    game.player2_wins_point()
    game.player2_wins_point()
    game.player2_wins_point()
    assert game.winner() == "Player 2"  # Player 2 wins after scoring beyond "40"

def test_no_winner_with_less_than_four_points():
    game = TennisGame()
    game.player1_wins_point()
    game.player2_wins_point()
    assert game.winner() is None  # No winner yet, both players below "40"

def test_deuce_and_advantage():
    game = TennisGame()
    game.player1_wins_point()
    game.player1_wins_point()
    game.player1_wins_point()  # Player 1: 40
    game.player2_wins_point()
    game.player2_wins_point()  # Player 2: 40
    assert game.score() == ("40", "40")  # Both players at "40"

    game.player1_wins_point()
    assert game.score() == ("A", "40")  # Player 1 has advantage

    game.player2_wins_point()
    assert game.score() == ("40", "40")  # Back to deuce

    game.player2_wins_point()
    game.player2_wins_point()  # Player 2: 40
    game.player1_wins_point()
    assert game.score() == ("40", "A")  # Player 2 has advantage

    game.player2_wins_point()
    assert game.winner() == "Player 2"  # Player 2 wins with advantage

def test_player_1_wins_after_advantage():
    game = TennisGame()
    game.player1_wins_point()
    game.player1_wins_point()
    game.player1_wins_point()  # Player 1: 40
    game.player2_wins_point()
    game.player2_wins_point()  # Player 2: 40
    assert game.score() == ("40", "40")  # Both players at "40"

    game.player1_wins_point()
    assert game.score() == ("A", "40")  # Player 1 has advantage

    game.player1_wins_point()
    assert game.winner() == "Player 1"  # Player 1 wins after advantage

def test_player_2_wins_after_advantage():
    game = TennisGame()
    game.player1_wins_point()
    game.player1_wins_point()
    game.player1_wins_point()  # Player 1: 40
    game.player2_wins_point()
    game.player2_wins_point()  # Player 2: 40
    assert game.score() == ("40", "40")  # Both players at "40"

    game.player2_wins_point()
    assert game.score() == ("40", "A")  # Player 2 has advantage

    game.player2_wins_point()
    assert game.winner() == "Player 2"  # Player 2 wins after advantage

def test_no_winner_at_40_40():
    game = TennisGame()
    game.player1_wins_point()
    game.player1_wins_point()
    game.player1_wins_point()  # Player 1: 40
    game.player2_wins_point()
    game.player2_wins_point()  # Player 2: 40
    assert game.winner() is None  # No winner at 40-40

def test_repeated_deuce_scenario():
    game = TennisGame()
    game.player1_wins_point()
    game.player1_wins_point()
    game.player1_wins_point()  # Player 1: 40
    game.player2_wins_point()
    game.player2_wins_point()  # Player 2: 40
    assert game.score() == ("40", "40")  # Both players at "40"

    game.player1_wins_point()
    assert game.score() == ("A", "40")  # Player 1 has advantage

    game.player2_wins_point()
    assert game.score() == ("40", "40")  # Back to deuce

    game.player2_wins_point()
    game.player2_wins_point()  # Player 2: 40
    game.player1_wins_point()
    assert game.score() == ("40", "A")  # Player 2 has advantage

    game.player1_wins_point()
    assert game.score() == ("40", "40")  # Back to deuce again

    game.player2_wins_point()
    assert game.winner() is None  # No winner yet