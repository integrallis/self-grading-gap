def calculate_score(rolls):
    score = 0
    frame = 0
    roll_index = 0
    while frame < 10:
        if roll_index >= len(rolls):  # If there are no more rolls
            break
        if rolls[roll_index] == 10:  # Strike
            score += 10 + (rolls[roll_index + 1] if roll_index + 1 < len(rolls) else 0) + (rolls[roll_index + 2] if roll_index + 2 < len(rolls) else 0)
            frame += 1
            roll_index += 1
        elif roll_index + 1 < len(rolls) and rolls[roll_index] + rolls[roll_index + 1] == 10:  # Spare
            score += 10 + (rolls[roll_index + 2] if roll_index + 2 < len(rolls) else 0)
            frame += 1
            roll_index += 2
        else:  # Open frame
            if roll_index + 1 < len(rolls):
                score += rolls[roll_index] + rolls[roll_index + 1]
            else:
                score += rolls[roll_index]
            frame += 1
            roll_index += 2
    return score
