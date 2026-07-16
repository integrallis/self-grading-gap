# candidate/impl.py

class BowlingGame:
    def __init__(self):
        self.rolls = []
        
    def roll(self, pins):
        if pins < 0 or pins > 10:
            raise ValueError("Pins must be between 0 and 10")
        self.rolls.append(pins)
        
    def score(self):
        total_score = 0
        roll_index = 0
        
        for frame in range(10):
            if self.is_strike(roll_index):  # Strike
                total_score += 10 + self.strike_bonus(roll_index)
                roll_index += 1
            elif self.is_spare(roll_index):  # Spare
                total_score += 10 + self.spare_bonus(roll_index)
                roll_index += 2
            else:  # Open frame
                total_score += self.open_frame_score(roll_index)
                roll_index += 2
                
        return total_score
    
    def is_strike(self, roll_index):
        return self.rolls[roll_index] == 10
    
    def is_spare(self, roll_index):
        return self.rolls[roll_index] + self.rolls[roll_index + 1] == 10
    
    def strike_bonus(self, roll_index):
        return self.rolls[roll_index + 1] + (self.rolls[roll_index + 2] if roll_index + 2 < len(self.rolls) else 0)
    
    def spare_bonus(self, roll_index):
        return self.rolls[roll_index + 2] if roll_index + 2 < len(self.rolls) else 0
    
    def open_frame_score(self, roll_index):
        return self.rolls[roll_index] + self.rolls[roll_index + 1]
