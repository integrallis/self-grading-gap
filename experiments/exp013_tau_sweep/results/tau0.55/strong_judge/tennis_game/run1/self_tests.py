from solution import TennisGame

def test_initial_scores_are_zero():
    game = TennisGame()
    assert game.score() == ("0", "0")  # AC-2.1: Both players start at "0"

def test_player_one_scores_first_point():
    game = TennisGame()
    game.player_one_scores()
    assert game.score() == ("15", "0")  # Player one has 1 point, announced as "15"

def test_player_two_scores_first_point():
    game = TennisGame()
    game.player_two_scores()
    assert game.score() == ("0", "15")  # Player two has 1 point, announced as "15"

def test_player_one_scores_second_point():
    game = TennisGame()
    game.player_one_scores()
    game.player_one_scores()
    assert game.score() == ("30", "0")  # Player one has 2 points, announced as "30"

def test_player_two_scores_to_thirty():
    game = TennisGame()
    game.player_two_scores()
    game.player_two_scores()
    assert game.score() == ("0", "30")  # Player two has 2 points, announced as "30"

def test_player_one_wins_game_from_forty():
    game = TennisGame()
    game.player_one_scores()
    game.player_one_scores()
    game.player_one_scores()  # Player one at "40"
    game.player_one_scores()  # Player one wins
    assert game.score() == ("0", "0")  # Winner is declared, score resets

def test_game_reports_no_winner_if_points_less_than_four():
    game = TennisGame()
    game.player_one_scores()
    game.player_two_scores()
    assert game.score() == ("15", "15")  # Neither player has won, score is "15" each

def test_deuce_and_advantage():
    game = TennisGame()
    game.player_one_scores()  # 15
    game.player_two_scores()  # 15
    game.player_one_scores()  # 30
    game.player_two_scores()  # 30
    game.player_one_scores()  # 40
    game.player_two_scores()  # 40
    game.player_one_scores()  # Advantage for player one
    assert game.score() == ("A", "40")  # AC-4.1: Player one has advantage
    assert game.score() == ("A", "40")  # Still no winner

def test_return_to_deuce_from_advantage():
    game = TennisGame()
    game.player_one_scores()  # 15
    game.player_two_scores()  # 15
    game.player_one_scores()  # 30
    game.player_two_scores()  # 30
    game.player_one_scores()  # 40
    game.player_two_scores()  # 40
    game.player_one_scores()  # Advantage for player one
    game.player_two_scores()  # Back to deuce
    assert game.score() == ("40", "40")  # AC-4.2: Return to deuce

def test_player_with_advantage_wins_game():
    game = TennisGame()
    game.player_one_scores()  # 15
    game.player_two_scores()  # 15
    game.player_one_scores()  # 30
    game.player_two_scores()  # 30
    game.player_one_scores()  # 40
    game.player_two_scores()  # 40
    game.player_one_scores()  # Advantage for player one
    game.player_one_scores()  # Player one wins
    assert game.score() == ("0", "0")  # Winner is declared, score resets

def test_player_two_wins_game_from_forty():
    game = TennisGame()
    game.player_two_scores()  # 15
    game.player_two_scores()  # 30
    game.player_two_scores()  # 40
    game.player_two_scores()  # Player two wins
    assert game.score() == ("0", "0")  # Winner is declared, score resets

def test_player_one_on_forty_with_player_two_on_zero():
    game = TennisGame()
    game.player_one_scores()  # 15
    game.player_one_scores()  # 30
    game.player_one_scores()  # 40
    assert game.score() == ("40", "0")  # AC-4.4: Player one is at 40, player two at 0

def test_deuce_cycle():
    game = TennisGame()
    game.player_one_scores()  # 15
    game.player_two_scores()  # 15
    game.player_one_scores()  # 30
    game.player_two_scores()  # 30
    game.player_one_scores()  # 40
    game.player_two_scores()  # 40
    game.player_one_scores()  # Advantage for player one
    game.player_two_scores()  # Back to deuce
    assert game.score() == ("40", "40")  # Back to deuce
    game.player_two_scores()  # Advantage for player two
    assert game.score() == ("40", "A")  # Player two has advantage
    game.player_one_scores()  # Back to deuce
    assert game.score() == ("40", "40")  # Back to deuce again