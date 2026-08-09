# file: bowling_game/game.py
from candidate import calculate_score


class Game:
    def __init__(self):
        self.rolls = []

    def roll(self, pins):
        self.rolls.append(pins)

    def score(self):
        return calculate_score(self.rolls)
