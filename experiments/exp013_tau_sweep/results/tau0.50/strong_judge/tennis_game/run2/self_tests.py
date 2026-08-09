from solution import TennisGame

def test_initial_scores_are_zero():
    game = TennisGame()
    assert game.score() == ("0", "0")  # Initial scores are both 0

def test_player_one_wins_first_point():
    game = TennisGame()
    game.player_one_wins_point()
    assert game.score() == ("15", "0")  # Player one moves to 15, player two remains at 0

def test_player_two_wins_first_point():
    game = TennisGame()
    game.player_two_wins_point()
    assert game.score() == ("0", "15")  # Player two moves to 15, player one remains at 0

def test_player_one_wins_points_to_thirty():
    game = TennisGame()
    game.player_one_wins_point()
    game.player_one_wins_point()  # 15 to 30
    assert game.score() == ("30", "0")  # Player one at 30, player two at 0

def test_player_one_wins_point_to_forty():
    game = TennisGame()
    game.player_one_wins_point()
    game.player_one_wins_point()  # 15 to 30
    game.player_one_wins_point()  # 30 to 40
    assert game.score() == ("40", "0")  # Player one at 40, player two at 0

def test_player_one_wins_game_after_forty():
    game = TennisGame()
    game.player_one_wins_point()
    game.player_one_wins_point()  # 15 to 30
    game.player_one_wins_point()  # 30 to 40
    game.player_one_wins_point()  # Player one wins
    assert game.winner() == "Player 1"  # Player one wins the game

def test_player_two_wins_game_after_forty():
    game = TennisGame()
    game.player_two_wins_point()
    game.player_two_wins_point()  # 15 to 30
    game.player_two_wins_point()  # 30 to 40
    game.player_two_wins_point()  # Player two wins
    assert game.winner() == "Player 2"  # Player two wins the game

def test_no_winner_with_both_at_forty():
    game = TennisGame()
    game.player_one_wins_point()
    game.player_one_wins_point()  # 15 to 30
    game.player_one_wins_point()  # 30 to 40
    game.player_two_wins_point()  # Player two also to 40
    assert game.winner() is None  # No winner yet, both at 40

def test_deuce_and_advantage():
    game = TennisGame()
    game.player_one_wins_point()  # 15 to 0
    game.player_one_wins_point()  # 30 to 0
    game.player_one_wins_point()  # 40 to 0
    game.player_two_wins_point()  # Player two to 15
    game.player_two_wins_point()  # Player two to 30
    game.player_two_wins_point()  # Player two to 40
    game.player_two_wins_point()  # Player two wins point, both at 40
    assert game.score() == ("40", "A")  # Player two has advantage
    assert game.winner() is None  # Still no winner
    game.player_two_wins_point()  # Player two wins
    assert game.winner() == "Player 2"  # Player two wins the game

def test_return_to_deuce_from_advantage():
    game = TennisGame()
    game.player_one_wins_point()  # 15 to 0
    game.player_one_wins_point()  # 30 to 0
    game.player_one_wins_point()  # 40 to 0
    game.player_two_wins_point()  # Player two to 15
    game.player_two_wins_point()  # Player two to 30
    game.player_two_wins_point()  # Player two to 40
    game.player_two_wins_point()  # Player two wins point, both at 40
    assert game.score() == ("40", "A")  # Player two has advantage
    game.player_one_wins_point()  # Player one returns to deuce
    assert game.score() == ("40", "40")  # Both at deuce again

def test_multi_cycle_deuce():
    game = TennisGame()
    game.player_one_wins_point()  # 15 to 0
    game.player_one_wins_point()  # 30 to 0
    game.player_one_wins_point()  # 40 to 0
    game.player_two_wins_point()  # Player two to 15
    game.player_two_wins_point()  # Player two to 30
    game.player_two_wins_point()  # Player two to 40
    game.player_two.wins_point()  # Player two wins point, both at 40
    assert game.score() == ("40", "A")  # Player two has advantage
    assert game.winner() is None  # Still no winner
    game.player_two_wins_point()  # Player two wins
    assert game.winner() == "Player 2"  # Player two wins the game

def test_forty_zero_scenario():
    game = TennisGame()
    game.player_one_wins_point()  # 15 to 0
    game.player_one_wins_point()  # 30 to 0
    game.player_one_wins_point()  # 40 to 0
    game.player_two_wins_point()  # Player two to 15
    assert game.score() == ("40", "15")  # Player one at 40, player two at 15