# file: darts/game.py
from candidate import DartsGame


class Multiplier:
    @staticmethod
    def SINGLE(game, value):
        return game.throw_dart(value)

    @staticmethod
    def DOUBLE(game, value):
        return game.throw_dart(value, double=True)

    @staticmethod
    def TRIPLE(game, value):
        return game.throw_dart(value, triple=True)


class Darts:
    def __init__(self):
        self._game = DartsGame()

    def dart(self, value, multiplier=Multiplier.SINGLE):
        return multiplier(self._game, value)

    def darts_left(self):
        return self._game.darts_remaining

    def get_turn(self):
        return self._game.turn

    def is_finished(self):
        return self._game.finished

    def score(self):
        return self._game.score
