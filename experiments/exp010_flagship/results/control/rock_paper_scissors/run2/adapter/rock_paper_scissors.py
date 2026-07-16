# file: rock_paper_scissors.py
from candidate import judge_round as play


class Move:
    ROCK = "ROCK"
    PAPER = "PAPER"
    SCISSORS = "SCISSORS"
    LIZARD = "LIZARD"
    SPOCK = "SPOCK"


class Outcome:
    TIE = "TIE"
    PLAYER_WINS = "PLAYER_WINS"
    PLAYER_LOSES = "PLAYER_LOSES"
