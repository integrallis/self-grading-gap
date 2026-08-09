# test_tennis.py

from solution import TennisGame

def test_initial_score():
    game = TennisGame()
    assert game.score() == ("0", "0")  # AC-2.1: New game starts with both players at "0"

def test_player_1_wins_first_point():
    game = TennisGame()
    game.player_1_scores()
    assert game.score() == ("15", "0")  # AC-2.2: Player 1 wins a point, score advances to "15"

def test_player_2_wins_first_point():
    game = TennisGame()
    game.player_2_scores()
    assert game.score() == ("0", "15")  # AC-2.2: Player 2 wins a point, score advances to "15"

def test_player_1_wins_second_point():
    game = TennisGame()
    game.player_1_scores()  # 15-0
    game.player_1_scores()  # 30-0
    assert game.score() == ("30", "0")  # Player 1 wins another point

def test_player_1_wins_to_40():
    game = TennisGame()
    game.player_1_scores()  # 0-0
    game.player_1_scores()  # 15-0
    game.player_1_scores()  # 30-0
    game.player_1_scores()  # 40-0
    assert game.score() == ("40", "0")  # Player 1 reaches "40"

def test_player_1_wins_game_from_40():
    game = TennisGame()
    game.player_1_scores()  # 0-0
    game.player_1_scores()  # 15-0
    game.player_1_scores()  # 30-0
    game.player_1_scores()  # 40-0
    assert game.winner() == "None"  # AC-3.1: No winner yet
    game.player_2_scores()  # 40-15
    game.player_1_scores()  # Player 1 wins game
    assert game.winner() == "Player 1"  # AC-3.2: Player 1 wins the game

def test_deuce_and_advantage():
    game = TennisGame()
    for _ in range(3):
        game.player_1_scores()  # Player 1 to 40
        game.player_2_scores()  # Player 2 to 40
    assert game.score() == ("40", "40")  # AC-4.1: Both players at "40"
    
    game.player_1_scores()  # Player 1 has advantage
    assert game.score() == ("A", "40")  # AC-4.1: Player 1 has advantage
    assert game.winner() == "None"  # Still no winner

    game.player_2_scores()  # Back to deuce
    assert game.score() == ("40", "40")  # AC-4.2: Back to deuce

    game.player_1_scores()  # Player 1 has advantage again
    assert game.score() == ("A", "40")  # Player 1 has advantage
    
    game.player_1_scores()  # Player 1 wins game
    assert game.winner() == "Player 1"  # AC-4.3: Player 1 wins

def test_player_2_wins_game_from_40():
    game = TennisGame()
    game.player_2_scores()  # 0-0
    game.player_2_scores()  # 0-15
    game.player_2_scores()  # 0-30
    game.player_2_scores()  # 0-40
    assert game.winner() == "Player 2"  # Player 2 wins the game

def test_no_winner_at_40_15():
    game = TennisGame()
    game.player_1_scores()  # 0-0
    game.player_1_scores()  # 15-0
    game.player_2_scores()  # 15-15
    game.player_1_scores()  # 30-15
    game.player_2_scores()  # 30-30
    game.player_1_scores()  # 40-30
    assert game.score() == ("40", "15")  # Player 1 at "40", Player 2 at "15"
    assert game.winner() == "None"  # No winner yet

def test_player_2_advantage_to_win():
    game = TennisGame()
    for _ in range(3):
        game.player_2_scores()  # Player 2 to 40
        game.player_1_scores()  # Player 1 to 40
    assert game.score() == ("40", "40")  # Both players at "40"

    game.player_2_scores()  # Player 2 has advantage
    assert game.score() == ("40", "A")  # Player 2 has advantage
    assert game.winner() == "None"  # Still no winner

    game.player_2_scores()  # Player 2 wins game
    assert game.winner() == "Player 2"  # Player 2 wins the game

def test_repeated_deuce_advantage():
    game = TennisGame()
    for _ in range(3):
        game.player_1_scores()  # Player 1 to 40
        game.player_2_scores()  # Player 2 to 40
    assert game.score() == ("40", "40")  # Both players at "40"

    game.player_1_scores()  # Player 1 has advantage
    assert game.score() == ("A", "40")  # Player 1 has advantage
    game.player_2_scores()  # Back to deuce
    assert game.score() == ("40", "40")  # Back to deuce again

    game.player_2_scores()  # Player 2 has advantage
    assert game.score() == ("40", "A")  # Player 2 has advantage
    game.player_1_scores()  # Back to deuce again
    assert game.score() == ("40", "40")  # Back to deuce again

def test_player_1_leads_at_40():
    game = TennisGame()
    game.player_1_scores()  # 0-0
    game.player_1_scores()  # 15-0
    game.player_1_scores()  # 30-0
    game.player_1_scores()  # 40-0
    assert game.score() == ("40", "0")  # Player 1 should be at "40"
    assert game.winner() == "None"  # No winner yet