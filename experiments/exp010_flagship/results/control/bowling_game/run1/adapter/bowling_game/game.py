# file: bowling_game/game.py
from candidate import calculate_score


class Game:
    def __init__(self):
        self._rolls = []

    def roll(self, pins):
        self._rolls.append(pins)

    def score(self):
        return calculate_score(self._rolls)
