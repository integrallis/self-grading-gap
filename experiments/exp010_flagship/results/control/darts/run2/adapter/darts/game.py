# file: darts/game.py
from candidate import start_game, throw_dart


class _Single:
    def apply(self, game, value):
        return throw_dart(game, value)


class _Double:
    def apply(self, game, value):
        return throw_dart(game, value, is_double=True)


class _Triple:
    def apply(self, game, value):
        return throw_dart(game, value, is_triple=True)


class Multiplier:
    SINGLE = _Single()
    DOUBLE = _Double()
    TRIPLE = _Triple()


class Darts:
    def __init__(self):
        self._game = start_game()

    def dart(self, value, multiplier=Multiplier.SINGLE):
        self._game = multiplier.apply(self._game, value)

    def darts_left(self):
        return self._game.get("darts_remaining")

    def get_turn(self):
        return self._game.get("turn")

    def is_finished(self):
        return self._game.get("finished")

    def score(self):
        return self._game.get("score")
