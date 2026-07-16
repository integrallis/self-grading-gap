# file: tennis_game/tennis.py
from candidate import TennisGame


class Scores(TennisGame):
    def first_scores(self, *args):
        return self.player_one_scores()

    def second_scores(self, *args):
        return self.player_two_scores()

    def first_score(self):
        first, second = self.score()
        return first

    def second_score(self):
        first, second = self.score()
        return second

    def score_name(self, *args):
        return self.score()


Set = Scores
