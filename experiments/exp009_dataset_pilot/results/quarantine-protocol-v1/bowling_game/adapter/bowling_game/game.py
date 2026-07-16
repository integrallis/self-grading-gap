# file: bowling_game/game.py

from candidate.impl import BowlingGame

class Game:
    def __init__(self):
        self._game = BowlingGame()

    def roll(self, pins):
        self._game.roll(pins)

    def score(self):
        return self._game.score()
