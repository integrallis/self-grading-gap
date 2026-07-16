def calculate_score(rolls):
    if not rolls:
        return 0
    score = 0
    frame_index = 0
    for frame in range(10):  # There are 10 frames in a game
        if rolls[frame_index] == 10:  # Strike
            score += 10
            if frame_index + 1 < len(rolls):
                score += rolls[frame_index + 1]
            if frame_index + 2 < len(rolls):
                score += rolls[frame_index + 2]
            frame_index += 1
        elif frame_index + 1 < len(rolls) and rolls[frame_index] + rolls[frame_index + 1] == 10:  # Spare
            score += 10
            if frame_index + 2 < len(rolls):
                score += rolls[frame_index + 2]
            frame_index += 2
        else:  # Open frame
            score += rolls[frame_index] + rolls[frame_index + 1]
            frame_index += 2
    return score