class TennisGame:
    def __init__(self):
        self.points = [0, 0]
        self.score_names = ['0', '15', '30', '40']

    def player1_scores(self):
        self.points[0] += 1

    def player2_scores(self):
        self.points[1] += 1

    def score(self):
        p1_score = self.points[0]
        p2_score = self.points[1]

        if p1_score >= 3 and p2_score >= 3:
            if p1_score == p2_score:
                return ('40', '40')
            elif p1_score == p2_score + 1:
                return ('A', '40')
            elif p2_score == p1_score + 1:
                return ('40', 'A')

        return (self.score_names[p1_score], self.score_names[p2_score])

    def winner(self):
        if self.points[0] >= 4 and self.points[0] - self.points[1] >= 2:
            return "Player 1"
        elif self.points[1] >= 4 and self.points[1] - self.points[0] >= 2:
            return "Player 2"
        return None