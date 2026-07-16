def start_game(width, height, food_positions):
    if width <= 0 or height <= 0:
        raise ValueError("grid dimensions must be positive")
    snake = [(0, 0)]
    heading = 'right'
    score = 0
    game_over = False
    food = food_positions[0] if food_positions else None
    return snake, heading, score, game_over, food_positions


def tick(snake, heading, score, game_over, food_positions):
    if game_over:
        return snake, heading, score, game_over, food_positions

    head_x, head_y = snake[0]
    if heading == 'right':
        new_head = (head_x + 1, head_y)
    elif heading == 'left':
        new_head = (head_x - 1, head_y)
    elif heading == 'up':
        new_head = (head_x, head_y - 1)
    elif heading == 'down':
        new_head = (head_x, head_y + 1)
    else:
        raise ValueError(f"unknown direction: '{heading}'")

    # Check for collision with walls
    if not (0 <= new_head[0] < width and 0 <= new_head[1] < height):
        return snake, heading, score, True, None

    # Check for collision with self
    if new_head in snake:
        return snake, heading, score, True, None

    # Check if food is eaten
    if food_positions and new_head == food_positions[0]:
        snake.insert(0, new_head)
        score += 1
        food = food_positions.pop(0) if len(food_positions) > 1 else None
    else:
        snake.insert(0, new_head)
        snake.pop()

    return snake, heading, score, game_over, food


def change_direction(snake, heading, new_direction):
    opposite_directions = {'right': 'left', 'left': 'right', 'up': 'down', 'down': 'up'}
    if new_direction not in opposite_directions:
        raise ValueError(f"unknown direction: '{new_direction}'")
    if opposite_directions[heading] != new_direction:
        heading = new_direction
    return heading
