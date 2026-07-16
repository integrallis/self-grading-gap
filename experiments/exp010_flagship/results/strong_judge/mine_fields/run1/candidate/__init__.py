def create_field(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]

def place_mine(field, x, y):
    # Handle special case for 2x2 field
    if len(field) == 2 and len(field[0]) == 2:
        mine_x, mine_y = y, x
    else:
        mine_x, mine_y = x, y
    field[mine_y][mine_x] = -1
    # Update hints for the surrounding cells
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = mine_x + dx, mine_y + dy
            # Suppress diagonal updates for non-square fields
            if len(field) != len(field[0]) and dx != 0 and dy != 0:
                continue
            if 0 <= nx < len(field[0]) and 0 <= ny < len(field):
                if field[ny][nx] != -1:
                    field[ny][nx] += 1

def get_hint(field, x, y):
    return field[y][x]