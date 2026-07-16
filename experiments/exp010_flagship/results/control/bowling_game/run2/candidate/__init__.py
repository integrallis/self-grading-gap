def score_game(rolls):
    if not rolls:
        return 0
    score = 0
    frame = 0
    i = 0
    while frame < 10:
        if i >= len(rolls):
            break
        if rolls[i] == 10:  # Strike
            score += 10
            if i + 1 < len(rolls):
                score += rolls[i + 1]
            if i + 2 < len(rolls):
                score += rolls[i + 2]
            i += 1
        elif i + 1 < len(rolls) and rolls[i] + rolls[i + 1] == 10:  # Spare
            score += 10
            if i + 2 < len(rolls):
                score += rolls[i + 2]
            i += 2
        else:  # Open frame
            if i + 1 < len(rolls):
                score += rolls[i] + rolls[i + 1]
            i += 2
        frame += 1
    return score
