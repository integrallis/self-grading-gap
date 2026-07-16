# file: bowling_game/game.py

from candidate.impl import BowlingGame

class Game:
    def __init__(self):
        self.bowling_game = BowlingGame()
        
    def roll(self, pins):
        self.bowling_game.roll(pins)
        
    def score(self):
        return self.bowling_game.score()
