from solution import TennisGame

def test_initial_scores_are_zero():
    game = TennisGame()
    assert game.score() == ("0", "0")  # Both players start at 0

def test_player_one_scores_first_point():
    game = TennisGame()
    game.player_one_scores()
    assert game.score() == ("15", "0")  # Player 1 scores, Player 2 remains at 0

def test_player_two_scores_first_point():
    game = TennisGame()
    game.player_two_scores()
    assert game.score() == ("0", "15")  # Player 2 scores, Player 1 remains at 0

def test_player_one_scores_second_point():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    assert game.score() == ("30", "0")  # Player 1 is at 30, Player 2 remains at 0

def test_player_one_scores_multiple_points():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    assert game.score() == ("40", "0")  # Player 1 leads with 40, Player 2 at 0

def test_player_two_scores_multiple_points():
    game = TennisGame()
    game.player_two_scores()  # 0 -> 15
    game.player_two_scores()  # 15 -> 30
    game.player_two_scores()  # 30 -> 40
    assert game.score() == ("0", "40")  # Player 1 at 0, Player 2 leads with 40

def test_no_winner_initial_score():
    game = TennisGame()
    assert game.winner() is None  # No winner at the start

def test_no_winner_with_points():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_two_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    assert game.winner() is None  # No winner with scores 30-15

def test_player_one_wins_game_from_40():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    game.player_two_scores()   # 0 -> 15
    game.player_two_scores()   # 15 -> 30
    game.player_two_scores()   # 30 -> 40
    game.player_one_scores()   # Both at 40
    game.player_one_scores()   # Player 1 wins from "40" (not tied at 40)
    assert game.winner() == "Player 1"  # Player 1 wins the game

def test_player_two_wins_game_from_40():
    game = TennisGame()
    game.player_two_scores()  # 0 -> 15
    game.player_two_scores()  # 15 -> 30
    game.player_two_scores()  # 30 -> 40
    game.player_one_scores()   # 0 -> 15
    game.player_one_scores()   # 15 -> 30
    game.player_one_scores()   # 30 -> 40
    game.player_two_scores()   # Both at 40
    game.player_two_scores()   # Player 2 wins from "40" (not tied at 40)
    assert game.winner() == "Player 2"  # Player 2 wins the game

def test_game_stays_in_deuce():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    game.player_two_scores()   # 0 -> 15
    game.player_two_scores()   # 15 -> 30
    game.player_two_scores()   # 30 -> 40
    game.player_one_scores()   # Both at 40
    assert game.score() == ("40", "40")  # Both players at 40

def test_advance_to_advantage():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    game.player_two_scores()   # 0 -> 15
    game.player_two_scores()   # 15 -> 30
    game.player_two_scores()   # 30 -> 40
    game.player_one_scores()   # Both at 40
    game.player_one_scores()   # Player 1 gets advantage
    assert game.score() == ("A", "40")  # Player 1 has advantage
    assert game.winner() is None  # No winner at advantage

def test_return_to_deuce():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    game.player_two_scores()   # 0 -> 15
    game.player_two_scores()   # 15 -> 30
    game.player_two_scores()   # 30 -> 40
    game.player_one_scores()   # Both at 40
    game.player_one_scores()   # Player 1 gets advantage
    game.player_two_scores()   # Player 2 returns to deuce
    assert game.score() == ("40", "40")  # Both players back to deuce
    assert game.winner() is None  # No winner at deuce

def test_player_with_advantage_wins_game():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    game.player_two_scores()   # 0 -> 15
    game.player_two_scores()   # 15 -> 30
    game.player_two_scores()   # 30 -> 40
    game.player_one_scores()   # Both at 40
    game.player_one_scores()   # Player 1 gets advantage
    game.player_one_scores()   # Player 1 wins with advantage
    assert game.winner() == "Player 1"  # Player 1 wins the game

def test_advance_loss_to_deuce_cycle():
    game = TennisGame()
    game.player_one_scores()  # 0 -> 15
    game.player_one_scores()  # 15 -> 30
    game.player_one_scores()  # 30 -> 40
    game.player_two_scores()   # 0 -> 15
    game.player_two_scores()   # 15 -> 30
    game.player_two_scores()   # 30 -> 40
    game.player_one_scores()   # Both at 40
    game.player_one_scores()   # Player 1 gets advantage
    game.player_two_scores()   # Player 2 returns to deuce
    assert game.score() == ("40", "40")  # Both players back to deuce again
    assert game.winner() is None  # No winner at deuce