# file: tennis_game/tennis.py
from candidate import TennisGame


class Scores(TennisGame):
    def first_score(self):
        return next(iter(self.score()))

    def second_score(self):
        scores = iter(self.score())
        next(scores)
        return next(scores)

    def first_scores(self, score=None):
        return self.player_one_wins_point()

    def second_scores(self, score=None):
        return self.player_two_wins_point()

    def score_name(self, score):
        return self.score_map.get(score)


class Set(TennisGame):
    pass
