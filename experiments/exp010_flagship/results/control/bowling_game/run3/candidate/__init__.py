def score_bowling_game(rolls):
    score = 0
    frame_index = 0
    if not rolls:
        return 0
    for frame in range(10):  # There are 10 frames in bowling
        if frame_index >= len(rolls):
            break
        if rolls[frame_index] == 10:  # Strike
            if frame_index + 1 < len(rolls) and frame_index + 2 < len(rolls):
                score += 10 + rolls[frame_index + 1] + rolls[frame_index + 2]
            frame_index += 1
        elif frame_index + 1 < len(rolls) and rolls[frame_index] + rolls[frame_index + 1] == 10:  # Spare
            if frame_index + 2 < len(rolls):
                score += 10 + rolls[frame_index + 2]
            frame_index += 2
        else:
            if frame_index + 1 < len(rolls):
                score += rolls[frame_index] + rolls[frame_index + 1]
            frame_index += 2
    return score
