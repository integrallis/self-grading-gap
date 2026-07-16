def start_game():
    return [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]


def make_move(board, player, row, col):
    if board[row][col] == ' ':
        board[row][col] = player
    return board


def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None


def is_draw(board):
    return all(cell != ' ' for row in board for cell in row) and check_winner(board) is None
