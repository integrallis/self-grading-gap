# file: tennis_game/tennis.py
from candidate import TennisGame


class Scores(TennisGame):
    def first_score(self):
        return self.player1_scores()

    def first_scores(self, score=None):
        return self.player1_scores()

    def second_score(self):
        return self.player2_scores()

    def second_scores(self, score=None):
        return self.player2_scores()

    def score_name(self, score):
        return self.score_map.get(score)


class Set(Scores):
    pass
