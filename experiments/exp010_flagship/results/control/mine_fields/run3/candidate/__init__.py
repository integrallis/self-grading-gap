def create_field(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]


def get_hint(field_cell, field, row, col):
    if field_cell == -1:
        return -1
    return count_adjacent_mines(field, row, col)


def count_adjacent_mines(field, row, col):
    mine_count = 0
    for r in range(max(0, row - 1), min(len(field), row + 2)):
        for c in range(max(0, col - 1), min(len(field[0]), col + 2)):
            if field[r][c] == -1:
                mine_count += 1
    return mine_count
