def start_game():
    return [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

def make_move(game, row, col):
    if game[row][col] == ' ':
        game[row][col] = game['current_player']
        game['current_player'] = 'O' if game['current_player'] == 'X' else 'X'


def check_winner(game):
    # Check rows, columns, and diagonals
    for i in range(3):
        if game[i][0] == game[i][1] == game[i][2] != ' ':
            return game[i][0]  # Row win
        if game[0][i] == game[1][i] == game[2][i] != ' ':
            return game[0][i]  # Column win
    if game[0][0] == game[1][1] == game[2][2] != ' ':
        return game[0][0]  # Diagonal win
    if game[0][2] == game[1][1] == game[2][0] != ' ':
        return game[0][2]  # Diagonal win
    return None  # No winner yet

def is_draw(game):
    return all(cell != ' ' for row in game for cell in row) and check_winner(game) is None