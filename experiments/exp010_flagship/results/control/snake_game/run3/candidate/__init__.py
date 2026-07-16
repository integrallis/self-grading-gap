def start_game(width, height, food_positions):
    if width <= 0 or height <= 0:
        raise ValueError("grid dimensions must be positive")
    return {
        'snake': [(0, 0)],
        'heading': 'right',
        'score': 0,
        'game_over': False,
        'food': food_positions[0] if food_positions else None,
        'food_positions': food_positions
    }

def tick(game):
    if game['game_over']:
        return game
    width = game['food_positions'][0][0] if game['food_positions'] else 0
    height = game['food_positions'][0][1] if game['food_positions'] else 0
    x, y = game['snake'][0]
    if game['heading'] == 'right':
        x += 1
    elif game['heading'] == 'left':
        x -= 1
    elif game['heading'] == 'up':
        y -= 1
    elif game['heading'] == 'down':
        y += 1
    else:
        raise ValueError(f"unknown direction: '{game['heading']}'")

    # Check for collision with walls
    if x < 0 or x >= width or y < 0 or y >= height:
        game['game_over'] = True
        raise ValueError("game over")

    # Check for self collision
    if (x, y) in game['snake']:
        game['game_over'] = True
        raise ValueError("game over")

    # Move the snake
    new_head = (x, y)
    game['snake'].insert(0, new_head)

    # Check for food
    if game['food'] == new_head:
        game['score'] += 1
        game['food_positions'].pop(0)  # Remove food eaten
        game['food'] = game['food_positions'][0] if game['food_positions'] else None
    else:
        game['snake'].pop()  # Remove the tail

    return game

def change_heading(game, new_heading):
    opposite_directions = {
        'right': 'left',
        'left': 'right',
        'up': 'down',
        'down': 'up'
    }
    if new_heading not in opposite_directions:
        raise ValueError(f"unknown direction: '{new_heading}'")
    if game['heading'] != opposite_directions.get(new_heading):
        game['heading'] = new_heading
    return game
