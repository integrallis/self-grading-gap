def start_game():
    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    return board, 'X'

def make_move(board, current_player, row, col):
    if board[row][col] == ' ':
        board[row][col] = current_player
        next_player = 'O' if current_player == 'X' else 'X'
        return board, next_player
    return board, current_player  # Invalid move, same player stays

def check_winner(board):
    # Check rows, columns and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row) and check_winner(board) is None