def start_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    return board


def make_move(board, row, col, current_player):
    if board[row][col] == ' ':
        board[row][col] = current_player
        next_player = 'O' if current_player == 'X' else 'X'
        return board, next_player
    return board, current_player  # return the same player if the move is invalid


def check_winner(board):
    lines = [
        # Rows
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        # Columns
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        # Diagonals
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    for line in lines:
        if line[0] == line[1] == line[2] != ' ':
            return line[0]
    return None


def is_draw(board):
    return all(cell != ' ' for row in board for cell in row) and check_winner(board) is None
