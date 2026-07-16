# file: tennis_game/tennis.py
from candidate import TennisGame


class Scores(TennisGame):
    def first_score(self):
        return next(iter(self.score()))

    def second_score(self):
        scores = iter(self.score())
        next(scores)
        return next(scores)

    def first_scores(self, *args):
        return self.player1_scores()

    def second_scores(self, *args):
        return self.player2_scores()

    def score_name(self, *args):
        return self.score_names.__getitem__(*args)


class Set(Scores):
    pass
