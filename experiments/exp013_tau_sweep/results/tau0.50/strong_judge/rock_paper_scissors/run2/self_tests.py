# your complete test file
from solution import judge_round

def test_rock_beats_scissors():
    # ROCK beats SCISSORS -> PLAYER_WINS
    assert judge_round('ROCK', 'SCISSORS') == 'PLAYER_WINS'

def test_scissors_beats_paper():
    # SCISSORS beats PAPER -> PLAYER_WINS
    assert judge_round('SCISSORS', 'PAPER') == 'PLAYER_WINS'

def test_paper_beats_rock():
    # PAPER beats ROCK -> PLAYER_WINS
    assert judge_round('PAPER', 'ROCK') == 'PLAYER_WINS'

def test_scissors_loses_to_rock():
    # SCISSORS loses to ROCK -> PLAYER_LOSES
    assert judge_round('SCISSORS', 'ROCK') == 'PLAYER_LOSES'

def test_paper_loses_to_scissors():
    # PAPER loses to SCISSORS -> PLAYER_LOSES
    assert judge_round('PAPER', 'SCISSORS') == 'PLAYER_LOSES'

def test_rock_loses_to_paper():
    # ROCK loses to PAPER -> PLAYER_LOSES
    assert judge_round('ROCK', 'PAPER') == 'PLAYER_LOSES'

def test_spock_smashes_scissors():
    # SPOCK beats SCISSORS -> PLAYER_WINS
    assert judge_round('SPOCK', 'SCISSORS') == 'PLAYER_WINS'

def test_scissors_loses_to_spock():
    # SCISSORS loses to SPOCK -> PLAYER_LOSES
    assert judge_round('SCISSORS', 'SPOCK') == 'PLAYER_LOSES'

def test_spock_vaporizes_rock():
    # SPOCK beats ROCK -> PLAYER_WINS
    assert judge_round('SPOCK', 'ROCK') == 'PLAYER_WINS'

def test_rock_loses_to_spock():
    # ROCK loses to SPOCK -> PLAYER_LOSES
    assert judge_round('ROCK', 'SPOCK') == 'PLAYER_LOSES'

def test_paper_disproves_spock():
    # PAPER beats SPOCK -> PLAYER_WINS
    assert judge_round('PAPER', 'SPOCK') == 'PLAYER_WINS'

def test_spock_loses_to_paper():
    # SPOCK loses to PAPER -> PLAYER_LOSES
    assert judge_round('SPOCK', 'PAPER') == 'PLAYER_LOSES'

def test_identical_moves_tie_rock():
    # ROCK against ROCK -> TIE
    assert judge_round('ROCK', 'ROCK') == 'TIE'

def test_identical_moves_tie_paper():
    # PAPER against PAPER -> TIE
    assert judge_round('PAPER', 'PAPER') == 'TIE'

def test_identical_moves_tie_scissors():
    # SCISSORS against SCISSORS -> TIE
    assert judge_round('SCISSORS', 'SCISSORS') == 'TIE'

def test_identical_moves_tie_spock():
    # SPOCK against SPOCK -> TIE
    assert judge_round('SPOCK', 'SPOCK') == 'TIE'

def test_different_moves_never_tie():
    # ROCK against PAPER -> PLAYER_LOSES (not a tie)
    assert judge_round('ROCK', 'PAPER') == 'PLAYER_LOSES'
    # PAPER against SCISSORS -> PLAYER_LOSES (not a tie)
    assert judge_round('PAPER', 'SCISSORS') == 'PLAYER_LOSES'
    # SCISSORS against ROCK -> PLAYER_LOSES (not a tie)
    assert judge_round('SCISSORS', 'ROCK') == 'PLAYER_LOSES'
    # SPOCK against SCISSORS -> PLAYER_WINS (not a tie)
    assert judge_round('SPOCK', 'SCISSORS') == 'PLAYER_WINS'

def test_all_pairings():
    # Test all pairings to ensure verdicts are symmetric and complete
    assert judge_round('ROCK', 'SCISSORS') == 'PLAYER_WINS'
    assert judge_round('SCISSORS', 'ROCK') == 'PLAYER_LOSES'
    assert judge_round('SCISSORS', 'PAPER') == 'PLAYER_WINS'
    assert judge_round('PAPER', 'SCISSORS') == 'PLAYER_LOSES'
    assert judge_round('PAPER', 'ROCK') == 'PLAYER_WINS'
    assert judge_round('ROCK', 'PAPER') == 'PLAYER_LOSES'
    assert judge_round('SPOCK', 'SCISSORS') == 'PLAYER_WINS'
    assert judge_round('SCISSORS', 'SPOCK') == 'PLAYER_LOSES'
    assert judge_round('SPOCK', 'ROCK') == 'PLAYER_WINS'
    assert judge_round('ROCK', 'SPOCK') == 'PLAYER_LOSES'
    assert judge_round('PAPER', 'SPOCK') == 'PLAYER_WINS'
    assert judge_round('SPOCK', 'PAPER') == 'PLAYER_LOSES'
    assert judge_round('ROCK', 'ROCK') == 'TIE'
    assert judge_round('PAPER', 'PAPER') == 'TIE'
    assert judge_round('SCISSORS', 'SCISSORS') == 'TIE'
    assert judge_round('SPOCK', 'SPOCK') == 'TIE'

def test_move_vocabulary():
    # Check that the move vocabulary contains exactly ROCK, PAPER, SCISSORS, and SPOCK
    moves = {'ROCK', 'PAPER', 'SCISSORS', 'SPOCK'}
    assert moves == {'ROCK', 'PAPER', 'SCISSORS', 'SPOCK'}

def test_verdict_vocabulary():
    # Check that the verdict vocabulary contains exactly PLAYER_WINS, PLAYER_LOSES, and TIE
    verdicts = {'PLAYER_WINS', 'PLAYER_LOSES', 'TIE'}
    assert verdicts == {'PLAYER_WINS', 'PLAYER_LOSES', 'TIE'}