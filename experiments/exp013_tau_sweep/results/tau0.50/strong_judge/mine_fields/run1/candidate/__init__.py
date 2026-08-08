def create_field(width, height):
    return [[0] * width for _ in range(height)]


def place_mine(field, x, y):
    field[y][x] = -1
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(field[0]) and 0 <= ny < len(field):
                if field[ny][nx] != -1:
                    field[ny][nx] += 1


def get_cell_hint(field, x, y):
    return field[y][x]