# file: darts/game.py
from candidate import start_game, throw_dart


class Multiplier:
    DOUBLE = "double"
    TRIPLE = "triple"


class Darts:
    def __init__(self):
        self._game = start_game()

    def dart(self, *args):
        self._game = throw_dart(self._game, *args)
        return self

    def darts_left(self):
        return self._game.get("darts_remaining")

    def get_turn(self):
        return self._game.get("turn")

    def is_finished(self):
        return self._game.get("finished")

    def score(self):
        return self._game.get("score")
