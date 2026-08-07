class TennisGame:
    def __init__(self):
        self.scores = [0, 0]

    def player1_scores(self):
        self.scores[0] += 1

    def player2_scores(self):
        self.scores[1] += 1

    def score(self):
        p1, p2 = self.scores
        if p1 >= 3 and p2 >= 3:
            if p1 == p2:
                return ("40", "40")
            if p1 == p2 + 1:
                return ("A", "40")
            if p2 == p1 + 1:
                return ("40", "A")
        labels = {0: "0", 1: "15", 2: "30", 3: "40"}
        return (labels[min(p1, 3)], labels[min(p2, 3)])

    def winner(self):
        if self.scores[0] >= 4 and self.scores[0] - self.scores[1] >= 2:
            return 1
        elif self.scores[1] >= 4 and self.scores[1] - self.scores[0] >= 2:
            return 2
        return None
