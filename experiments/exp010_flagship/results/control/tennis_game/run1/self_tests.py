from solution import TennisGame

def test_initial_scores_are_zero():
    game = TennisGame()
    assert game.score() == ("0", "0")  # Initial score is 0 for both players

def test_player_one_wins_first_point():
    game = TennisGame()
    game.player_one_wins_point()
    assert game.score() == ("15", "0")  # Player 1 scores, Player 2 remains at 0

def test_player_two_wins_first_point():
    game = TennisGame()
    game.player_two_wins_point()
    assert game.score() == ("0", "15")  # Player 2 scores, Player 1 remains at 0

def test_player_one_wins_second_point():
    game = TennisGame()
    game.player_one_wins_point()
    game.player_one_wins_point()
    assert game.score() == ("30", "0")  # Player 1 scores twice

def test_player_two_wins_second_point():
    game = TennisGame()
    game.player_two_wins_point()
    game.player_two_wins_point()
    assert game.score() == ("0", "30")  # Player 2 scores twice

def test_player_one_reaches_forty():
    game = TennisGame()
    game.player_one_wins_point()
    game.player_one_wins_point()
    game.player_one_wins_point()
    game.player_one_wins_point()
    assert game.score() == ("40", "0")  # Player 1 scores four times

def test_player_two_reaches_forty():
    game = TennisGame()
    game.player_two_wins_point()
    game.player_two_wins_point()
    game.player_two_wins_point()
    game.player_two_wins_point()
    assert game.score() == ("0", "40")  # Player 2 scores four times

def test_player_one_wins_game_from_forty():
    game = TennisGame()
    game.player_one_wins_point()
    game.player_one_wins_point()
    game.player_one_wins_point()
    game.player_one_wins_point()  # Player 1 reaches 40
    game.player_one_wins_point()  # Player 1 wins the game
    assert game.winner() == "Player 1"  # Player 1 wins the game

def test_no_winner_when_points_are_less_than_four():
    game = TennisGame()
    game.player_one_wins_point()
    game.player_two_wins_point()
    assert game.winner() is None  # No winner yet

def test_deuce_and_advantage():
    game = TennisGame()
    game.player_one_wins_point()
    game.player_one_wins_point()
    game.player_two_wins_point()
    game.player_two_wins_point()  # Both players are at 40 (deuce)
    game.player_one_wins_point()  # Player 1 has advantage
    assert game.score() == ("A", "40")  # Player 1 has advantage

def test_return_to_deuce():
    game = TennisGame()
    game.player_one_wins_point()
    game.player_one_wins_point()
    game.player_two_wins_point()
    game.player_two_wins_point()  # Both players are at 40 (deuce)
    game.player_one_wins_point()  # Player 1 has advantage
    game.player_two_wins_point()  # Player 2 wins the point, back to deuce
    assert game.score() == ("40", "40")  # Back to deuce

def test_player_with_advantage_wins_game():
    game = TennisGame()
    game.player_one_wins_point()
    game.player_one_wins_point()
    game.player_two_wins_point()
    game.player_two_wins_point()  # Both players are at 40 (deuce)
    game.player_one_wins_point()  # Player 1 has advantage
    game.player_one_wins_point()  # Player 1 wins the game
    assert game.winner() == "Player 1"  # Player 1 wins the game

def test_player_two_with_advantage_wins_game():
    game = TennisGame()
    game.player_one_wins_point()
    game.player_one_wins_point()
    game.player_two_wins_point()
    game.player_two_wins_point()  # Both players are at 40 (deuce)
    game.player_two_wins_point()  # Player 2 has advantage
    game.player_two_wins_point()  # Player 2 wins the game
    assert game.winner() == "Player 2"  # Player 2 wins the game

def test_player_on_forty_against_zero():
    game = TennisGame()
    game.player_one_wins_point()
    game.player_one_wins_point()
    game.player_one_wins_point()
    game.player_one_wins_point()  # Player 1 reaches 40
    game.player_two_wins_point()  # Player 2 is at 0
    assert game.score() == ("40", "0")  # Player 1 is at 40, Player 2 is at 0