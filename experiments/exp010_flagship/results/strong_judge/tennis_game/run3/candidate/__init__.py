class TennisGame:
    def __init__(self):
        self.player_one_points = 0
        self.player_two_points = 0

    def player_one_scores(self):
        self.player_one_points += 1

    def player_two_scores(self):
        self.player_two_points += 1

    def score(self):
        score_map = {0: '0', 1: '15', 2: '30', 3: '40'}
        if self.player_one_points >= 4 and self.player_one_points - self.player_two_points >= 2:
            return None, 1
        if self.player_two_points >= 4 and self.player_two_points - self.player_one_points >= 2:
            return None, 2

        if self.player_one_points >= 3 and self.player_two_points >= 3:
            if self.player_one_points == self.player_two_points:
                return '40', '40'
            elif self.player_one_points == self.player_two_points + 1:
                return 'A', '40'
            elif self.player_two_points == self.player_one_points + 1:
                return '40', 'A'

        return score_map[self.player_one_points], score_map[self.player_two_points]

    def winner(self):
        if self.player_one_points >= 4 and self.player_one_points - self.player_two_points >= 2:
            return 1
        if self.player_two_points >= 4 and self.player_two_points - self.player_one_points >= 2:
            return 2
        return None