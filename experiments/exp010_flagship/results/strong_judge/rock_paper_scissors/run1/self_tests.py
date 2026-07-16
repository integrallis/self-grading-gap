# test_solution.py

from solution import judge_round

def test_rock_beats_scissors():
    # Rock beats scissors
    assert judge_round('ROCK', 'SCISSORS') == 'PLAYER_WINS'
    # Scissors lose to rock
    assert judge_round('SCISSORS', 'ROCK') == 'PLAYER_LOSES'

def test_scissors_beat_paper():
    # Scissors beat paper
    assert judge_round('SCISSORS', 'PAPER') == 'PLAYER_WINS'
    # Paper loses to scissors
    assert judge_round('PAPER', 'SCISSORS') == 'PLAYER_LOSES'

def test_paper_beats_rock():
    # Paper beats rock
    assert judge_round('PAPER', 'ROCK') == 'PLAYER_WINS'
    # Rock loses to paper
    assert judge_round('ROCK', 'PAPER') == 'PLAYER_LOSES'

def test_spock_smashes_scissors():
    # Spock smashes scissors
    assert judge_round('SPOCK', 'SCISSORS') == 'PLAYER_WINS'
    # Scissors lose to Spock
    assert judge_round('SCISSORS', 'SPOCK') == 'PLAYER_LOSES'

def test_spock_vaporizes_rock():
    # Spock vaporizes rock
    assert judge_round('SPOCK', 'ROCK') == 'PLAYER_WINS'
    # Rock loses to Spock
    assert judge_round('ROCK', 'SPOCK') == 'PLAYER_LOSES'

def test_paper_disproves_spock():
    # Paper disproves Spock
    assert judge_round('PAPER', 'SPOCK') == 'PLAYER_WINS'
    # Spock loses to paper
    assert judge_round('SPOCK', 'PAPER') == 'PLAYER_LOSES'

def test_identical_moves_tie():
    # Identical moves tie
    assert judge_round('ROCK', 'ROCK') == 'TIE'
    assert judge_round('PAPER', 'PAPER') == 'TIE'
    assert judge_round('SCISSORS', 'SCISSORS') == 'TIE'
    assert judge_round('SPOCK', 'SPOCK') == 'TIE'

def test_differing_moves_never_tie():
    # Differing moves never tie
    assert judge_round('ROCK', 'PAPER') != 'TIE'
    assert judge_round('SCISSORS', 'ROCK') != 'TIE'
    assert judge_round('SPOCK', 'SCISSORS') != 'TIE'
    assert judge_round('PAPER', 'SPOCK') != 'TIE'

def test_available_moves():
    # Test that the available moves are exactly ROCK, PAPER, SCISSORS, and SPOCK
    assert judge_round('ROCK', 'PAPER') is not None  # Ensure ROCK is valid
    assert judge_round('PAPER', 'SCISSORS') is not None  # Ensure PAPER is valid
    assert judge_round('SCISSORS', 'SPOCK') is not None  # Ensure SCISSORS is valid
    assert judge_round('SPOCK', 'ROCK') is not None  # Ensure SPOCK is valid
    # Check that no other moves are valid
    invalid_moves = ['LIZARD', 'WATER', 'FIRE']
    for move in invalid_moves:
        assert judge_round(move, 'ROCK') is None
        assert judge_round('ROCK', move) is None

def test_available_verdicts():
    # Test that the available verdicts are exactly PLAYER_WINS, PLAYER_LOSES, and TIE
    assert judge_round('ROCK', 'SCISSORS') in ['PLAYER_WINS', 'PLAYER_LOSES', 'TIE']
    assert judge_round('SCISSORS', 'ROCK') in ['PLAYER_WINS', 'PLAYER_LOSES', 'TIE']
    assert judge_round('PAPER', 'ROCK') in ['PLAYER_WINS', 'PLAYER_LOSES', 'TIE']
    assert judge_round('ROCK', 'PAPER') in ['PLAYER_WINS', 'PLAYER_LOSES', 'TIE']
    assert judge_round('SPOCK', 'SCISSORS') in ['PLAYER_WINS', 'PLAYER_LOSES', 'TIE']
    assert judge_round('SCISSORS', 'SPOCK') in ['PLAYER_WINS', 'PLAYER_LOSES', 'TIE']
    assert judge_round('PAPER', 'SPOCK') in ['PLAYER_WINS', 'PLAYER_LOSES', 'TIE']
    assert judge_round('SPOCK', 'PAPER') in ['PLAYER_WINS', 'PLAYER_LOSES', 'TIE']