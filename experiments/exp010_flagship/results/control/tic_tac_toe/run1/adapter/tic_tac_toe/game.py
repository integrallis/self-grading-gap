# file: tic_tac_toe/game.py
from candidate import check_winner, is_draw, make_move, start_game


class TicTacToe:
    def __init__(self):
        self.board = start_game()
        self.current_player = 'X'

    def play(self, row, col):
        board = make_move(self.board, self.current_player, row, col)
        self.current_player = self.current_player.translate(
            str.maketrans('XO', 'OX')
        )
        return board

    def winner(self):
        return check_winner(self.board)

    def draw(self):
        return is_draw(self.board)
