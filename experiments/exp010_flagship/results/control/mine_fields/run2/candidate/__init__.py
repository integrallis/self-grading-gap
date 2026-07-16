def create_field(rows, cols, mines=[]):
    field = [[0 for _ in range(cols)] for _ in range(rows)]
    place_mines(field, mines)
    return field

def place_mines(field, mines):
    for (row, col) in mines:
        field[row][col] = -1

    for r in range(len(field)):
        for c in range(len(field[0])):
            if field[r][c] != -1:
                field[r][c] = count_adjacent_mines(field, r, c)


def count_adjacent_mines(field, row, col):
    if field[row][col] == -1:
        return -1
    adjacent_mines = 0
    for r in range(max(0, row - 1), min(len(field), row + 2)):
        for c in range(max(0, col - 1), min(len(field[0]), col + 2)):
            if field[r][c] == -1:
                adjacent_mines += 1
    return adjacent_mines


def get_hint(field, row, col):
    return field[row][col]