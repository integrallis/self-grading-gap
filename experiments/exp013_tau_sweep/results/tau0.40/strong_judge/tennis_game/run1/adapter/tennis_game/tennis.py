# file: tennis_game/tennis.py
from candidate import TennisGame


class Scores(TennisGame):
    def first_score(self):
        first, second = self.score()
        return first

    def second_score(self):
        first, second = self.score()
        return second

    def first_scores(self, *arguments):
        return self.player1_scores(*arguments)

    def second_scores(self, *arguments):
        return self.player2_scores(*arguments)

    def score_name(self, *arguments):
        return self.score(*arguments)


class Set(Scores):
    pass
