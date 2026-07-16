class TennisGame:
    def __init__(self):
        self.points = [0, 0]
        self.score_map = {0: "0", 1: "15", 2: "30", 3: "40"}

    def player1_scores(self):
        self.points[0] += 1

    def player2_scores(self):
        self.points[1] += 1

    def score(self):
        score1 = self.score_map.get(self.points[0], "A")
        score2 = self.score_map.get(self.points[1], "A")
        if score1 == "A":
            score2 = "40" if self.points[1] >= 3 else score2
        if score2 == "A":
            score1 = "40" if self.points[0] >= 3 else score1
        return score1, score2

    def winner(self):
        if self.points[0] >= 4 and self.points[0] - self.points[1] >= 2:
            return 1
        if self.points[1] >= 4 and self.points[1] - self.points[0] >= 2:
            return 2
        if self.points[0] == 4 and self.points[1] == 3:
            return None  # Player 1 has advantage but hasn't won yet
        if self.points[1] == 4 and self.points[0] == 3:
            return None  # Player 2 has advantage but hasn't won yet
        return None