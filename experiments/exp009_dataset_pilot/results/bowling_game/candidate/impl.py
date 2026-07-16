# candidate/impl.py

class BowlingGame:
    def __init__(self):
        self.rolls = []
    
    def roll(self, pins):
        self.rolls.append(pins)
    
    def score(self):
        total_score = 0
        frame_index = 0
        for frame in range(10):
            if self.is_strike(frame_index):  # Strike
                total_score += 10 + self.strike_bonus(frame_index)
                frame_index += 1
            elif self.is_spare(frame_index):  # Spare
                total_score += 10 + self.spare_bonus(frame_index)
                frame_index += 2
            else:  # Open frame
                total_score += self.open_frame_score(frame_index)
                frame_index += 2
        return total_score
    
    def is_strike(self, frame_index):
        return self.rolls[frame_index] == 10
    
    def is_spare(self, frame_index):
        return self.rolls[frame_index] + self.rolls[frame_index + 1] == 10
    
    def strike_bonus(self, frame_index):
        return self.rolls[frame_index + 1] + (self.rolls[frame_index + 2] if (frame_index + 2) < len(self.rolls) else 0)
    
    def spare_bonus(self, frame_index):
        return self.rolls[frame_index + 2] if (frame_index + 2) < len(self.rolls) else 0
    
    def open_frame_score(self, frame_index):
        return self.rolls[frame_index] + self.rolls[frame_index + 1]
