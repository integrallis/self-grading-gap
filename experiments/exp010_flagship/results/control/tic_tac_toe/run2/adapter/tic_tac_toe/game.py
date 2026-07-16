# file: tic_tac_toe/game.py
from candidate import check_winner
from candidate import is_draw
from candidate import make_move
from candidate import start_game


class TicTacToe:
    def __init__(self):
        self.board = start_game()
        self.current_player = 'X'

    def play(self, row, col):
        self.board, self.current_player = make_move(
            self.board,
            row,
            col,
            self.current_player,
        )
        return self.board

    def winner(self):
        return check_winner(self.board)

    def draw(self):
        return is_draw(self.board)
