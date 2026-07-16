class TennisGame:
    def __init__(self):
        self.points = [0, 0]
        self.score_map = {0: '0', 1: '15', 2: '30', 3: '40'}

    def player_one_wins_point(self):
        self.points[0] += 1

    def player_two_wins_point(self):
        self.points[1] += 1

    def score(self):
        if self.points[0] >= 4 or self.points[1] >= 4:
            if abs(self.points[0] - self.points[1]) >= 2:
                return (self.score_map[3] if self.points[0] > self.points[1] else '0',
                        self.score_map[3] if self.points[1] > self.points[0] else '0')
            if self.points[0] > self.points[1]:
                return ('A', self.score_map[self.points[1]])
            if self.points[1] > self.points[0]:
                return (self.score_map[self.points[0]], 'A')
            return ('40', '40')  # Deuce

        return (self.score_map[self.points[0]], self.score_map[self.points[1]])

    def winner(self):
        if self.points[0] >= 4 or self.points[1] >= 4:
            if abs(self.points[0] - self.points[1]) >= 2:
                return "Player 1" if self.points[0] > self.points[1] else "Player 2"
        return None
