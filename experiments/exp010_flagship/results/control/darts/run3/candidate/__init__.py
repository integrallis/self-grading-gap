class DartsGame:
    def __init__(self):
        self.score = 301
        self.finished = False
        self.turn = 1
        self.darts_remaining = 3
        self.turn_score = 0
        self.starting_turn_score = self.score

    def throw_dart(self, value, double=False, triple=False):
        if self.finished:
            return

        if double:
            score_change = value * 2
        elif triple:
            score_change = value * 3
        else:
            score_change = value

        if self.score - score_change < 0:
            # Bust: Restore score and reset turn
            self.score = self.starting_turn_score
            self.turn_score = 0
            self.darts_remaining = 3
            return

        self.turn_score += score_change
        self.darts_remaining -= 1
        self.score -= score_change

        if self.darts_remaining == 0:
            if self.score == 0 and double:
                self.finished = True
            else:
                self.turn += 1
                self.darts_remaining = 3
                self.score += self.turn_score
                self.turn_score = 0
                self.starting_turn_score = self.score
