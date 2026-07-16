# file: bowling_game/game.py
from candidate import score_bowling_game


class Game:
    def __init__(self):
        self._rolls = list()

    def roll(self, pins):
        self._rolls.append(pins)

    def score(self):
        return score_bowling_game(self._rolls)
