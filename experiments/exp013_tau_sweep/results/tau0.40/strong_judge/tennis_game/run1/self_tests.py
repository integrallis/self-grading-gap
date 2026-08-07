from solution import TennisGame

def test_initial_scores():
    game = TennisGame()
    assert game.score() == ("0", "0")  # AC-2.1: New game starts at "0"

def test_player1_scores_first_point():
    game = TennisGame()
    game.player1_scores()
    assert game.score() == ("15", "0")  # AC-2.2: Player 1 moves to "15"

def test_player2_scores_first_point():
    game = TennisGame()
    game.player2_scores()
    assert game.score() == ("0", "15")  # AC-2.2: Player 2 moves to "15"

def test_player1_scores_two_points():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    assert game.score() == ("30", "0")  # Player 1 moves to "30"

def test_player2_scores_two_points():
    game = TennisGame()
    game.player2_scores()
    game.player2_scores()
    assert game.score() == ("0", "30")  # AC-4.4: Player 2 moves to "30"

def test_player1_scores_three_points():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()
    assert game.score() == ("40", "0")  # Player 1 moves to "40"

def test_player2_scores_three_points():
    game = TennisGame()
    game.player2_scores()
    game.player2_scores()
    game.player2_scores()
    assert game.score() == ("0", "40")  # Player 2 moves to "40"

def test_player1_wins_game_from_non_deuce_40():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()  # Player 1: 40
    game.player2_scores()
    game.player2_scores()  # Player 2: 30
    assert game.winner() is None  # AC-3.1: No winner yet
    game.player1_scores()  # Player 1 wins
    assert game.winner() == 1  # AC-3.2: Player 1 wins

def test_player2_wins_game_from_non_deuce_40():
    game = TennisGame()
    game.player2_scores()
    game.player2_scores()
    game.player2_scores()  # Player 2: 40
    game.player1_scores()  # Player 1: 15
    assert game.winner() is None  # AC-3.1: No winner yet
    game.player2_scores()  # Player 2 wins
    assert game.winner() == 2  # AC-3.2: Player 2 wins

def test_deuce_to_advantage():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()
    game.player2_scores()
    game.player2_scores()
    game.player2_scores()
    game.player1_scores()  # Both at 40
    assert game.score() == ("A", "40")  # AC-4.1: Player 1 has advantage

def test_player2_advantage():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player2_scores()
    game.player2_scores()
    game.player2_scores()  # Both at 40
    game.player1_scores()  # Back to deuce
    game.player2_scores()  # Player 2 has advantage
    assert game.score() == ("40", "A")  # Player 2 has advantage

def test_advantage_back_to_deuce():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()
    game.player2_scores()
    game.player2_scores()
    game.player2_scores()
    game.player1_scores()  # Both at 40
    game.player2_scores()  # Back to deuce
    assert game.score() == ("40", "40")  # AC-4.2: Back to deuce

def test_player_with_advantage_wins():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()
    game.player2_scores()
    game.player2_scores()
    game.player2_scores()
    game.player1_scores()  # Both at 40
    game.player2_scores()  # Back to deuce
    game.player1_scores()  # Player 1 has advantage
    assert game.winner() is None  # Still no winner
    game.player1_scores()  # Player 1 wins
    assert game.winner() == 1  # AC-4.3: Player 1 wins

def test_advantage_does_not_count_when_opponent_on_0():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()
    game.player2_scores()
    game.player2_scores()
    game.player2_scores()
    game.player1_scores()  # Both at 40
    game.player2_scores()  # Back to deuce
    game.player1_scores()  # Player 1 has advantage
    assert game.score() == ("A", "40")  # Player 1 has advantage
    game.player2_scores()  # Player 2 scores, back to deuce
    assert game.score() == ("40", "40")  # Back to deuce

def test_repeated_deuce_cycle():
    game = TennisGame()
    game.player1_scores()
    game.player1_scores()
    game.player1_scores()
    game.player2_scores()
    game.player2_scores()
    game.player2_scores()
    game.player1_scores()  # Both at 40
    game.player2_scores()  # Back to deuce
    game.player1_scores()  # Player 1 has advantage
    game.player2_scores()  # Back to deuce again
    assert game.score() == ("40", "40")  # Back to deuce again
    game.player1_scores()  # Player 1 has advantage again
    game.player2_scores()  # Back to deuce once more
    assert game.score() == ("40", "40")  # Back to deuce once more